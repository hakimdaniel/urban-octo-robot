from flask import Flask, request
import requests

app = Flask(__name__)
BOT_TOKEN = os.getenv('BOT_TOKEN')

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").lower()

        if "hello" in text:
            send_message(chat_id, "Hi there!")
        elif "bye" in text:
            send_message(chat_id, "Goodbye!")
        else:
            send_message(chat_id, "I don't understand.")

    return "ok"
