from flask import Flask, request
from telegram import Bot, Update
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    try:
        data = request.get_json(force=True)
        print("DATA DARI TELEGRAM:", data)

        update = Update.de_json(data, bot)

        if update.message and update.message.text:
            chat_id = update.message.chat.id
            text = update.message.text
            print(f"[MSG] Chat ID: {chat_id}, Text: {text}")

            reply = f"Salam Boss! Kamu kata: {text}"
            await bot.send_message(chat_id=chat_id, text=reply)
            print("[OK] Mesej dihantar")
        else:
            print("[INFO] Tiada mesej teks.")

    except Exception as e:
        print("[ERROR]", e)

    return "ok"
