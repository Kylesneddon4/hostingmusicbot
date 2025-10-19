from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Discord bot is alive!"

def run():
    # Flask must listen on 0.0.0.0 so Render can reach it
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# This ensures it runs when you call python webserver.py directly
if __name__ == "__main__":
    keep_alive()
