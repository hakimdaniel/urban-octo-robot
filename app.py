from flask import Flask, request
from telegram import Bot, Update
import os

# Dapatkan token dari environment
TOKEN = os.getenv("BOT_TOKEN")

# Print token untuk debug (buang bila production)
print("TOKEN:", TOKEN)

bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        print("DATA DARI TELEGRAM:", data)

        update = Update.de_json(data, bot)

        if update.message and update.message.text:
            chat_id = update.message.chat.id
            text = update.message.text
            print(f"[MSG] Chat ID: {chat_id}, Text: {text}")

            reply = f"Salam Boss! Kamu kata: {text}"
            bot.send_message(chat_id=chat_id, text=reply)
            print("[OK] Mesej dihantar")
        else:
            print("[INFO] Tiada mesej teks.")

    except Exception as e:
        print("[ERROR]", e)

    return "ok"

if __name__ == "__main__":
    app.run(debug=False, port=5000)
