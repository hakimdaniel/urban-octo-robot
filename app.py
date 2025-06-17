from flask import Flask, request
import telegram
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/")
def index():
    return "This bot is running right now."

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("DATA DARI TELEGRAM:", data)

    update = telegram.Update.de_json(data, bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text
        print(f"MSG: {text}")

        reply = f"Salam Boss! Kamu kata: {text}"
        bot.send_message(chat_id=chat_id, text=reply)
    else:
        print("Tiada mesej dalam update")

    return 'ok'
