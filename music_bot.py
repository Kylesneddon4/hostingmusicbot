import discord
from discord.ext import commands
import yt_dlp
import os


DISCORD_TOKEN = os.environ['discordkey']

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Helper function to get YouTube audio URL ---
def get_youtube_audio_url(url):
    ydl_opts = {'format': 'bestaudio', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']

# --- Commands ---

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
            await ctx.send(f"Moved to {channel}")
        else:
            await channel.connect()
            await ctx.send(f"Joined {channel}")
    else:
        await ctx.send("You are not in a voice channel!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel!")

@bot.command()
async def play(ctx, url):
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel first!")
        return

    if not ctx.voice_client:
        await ctx.invoke(join)

    vc = ctx.voice_client
    if vc.is_playing():
        vc.stop()

    audio_url = get_youtube_audio_url(url)
    ffmpeg_opts = {'options': '-vn'}
    source = await discord.FFmpegOpusAudio.from_probe(audio_url, **ffmpeg_opts)
    vc.play(source, after=lambda e: print(f"Error: {e}") if e else None)
    await ctx.send(f"🎵 Now playing: {url}")

@bot.command()
async def stop(ctx):
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await ctx.send("⏹️ Stopped playback.")
    else:
        await ctx.send("No music is playing!")

@bot.command()
async def pause(ctx):
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await ctx.send("⏸️ Paused playback.")
    else:
        await ctx.send("No music is playing!")

@bot.command()
async def resume(ctx):
    vc = ctx.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send("▶️ Resumed playback.")
    else:
        await ctx.send("No music is paused!")

# --- Run the bot ---
bot.run("DISCORD_TOKEN")