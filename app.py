from flask import Flask, request
import os, requests

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID") or 7688576264)  # Ganti dengan chatid admin kau

# Simpan target sementara
pending_forward = {}

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def send_photo(chat_id, file_id, caption=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": file_id}
    if caption:
        payload["caption"] = caption
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text")
        photo = message.get("photo")

        # Hanya admin boleh akses
        if chat_id == ADMIN_ID:
            # Mula sesi forward ke target
            if text and text.startswith("/send "):
                try:
                    target_id = int(text.split(" ")[1])
                    pending_forward[chat_id] = target_id
                    send_message(chat_id, "📨 Send me any message or image to forward to target.")
                except:
                    send_message(chat_id, "❌ Invalid format. Guna: /send <chatid>")
                return "ok"

            # Kalau ada pending forward
            elif chat_id in pending_forward:
                target = pending_forward[chat_id]

                if photo:
                    file_id = photo[-1]["file_id"]  # Gambar resolusi tinggi
                    caption = message.get("caption")
                    send_photo(target, file_id, caption)
                elif text:
                    send_message(target, text)

                send_message(chat_id, f"✅ Forwarded to {target}")
                del pending_forward[chat_id]
                return "ok"

            # Jika bukan command
            else:
                send_message(chat_id, "❌ Guna arahan: /send <chatid>")
    
    return "ok"
