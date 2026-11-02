from flask import Flask, request
import os, requests

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID") # id kamu, misal 123456
LOG_CHANNEL = os.getenv("LOG_CHANNEL") or ADMIN_ID

def send(chat_id, text):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={"chat_id": chat_id, "text": text}, timeout=10)

@app.route("/", methods=["GET"])
def home():
    return "JogLend Support OK", 200

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True) or {}
    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text","") or msg.get("caption","")
        name = msg["from"].get("first_name","")
        username = msg["from"].get("username","-")

        if text.startswith("/start"):
            send(chat_id, 
"Hi! Selamat datang di Support @menfessangel 📩\n\n"
"Bot ini khusus untuk pengaduan, kritik & saran.\n"
"Segala masukan akan kami terima dengan bahasa yang membangun dan tidak menjatuhkan pihak manapun.\n\n"
"Ketik langsung keluhan / saran kamu di sini, admin akan baca.")
        elif text:
            # forward ke admin
            fwd_text = f"📩 SUPPORT BARU\nDari: {name} (@{username})\nID: {chat_id}\n\nIsi:\n{text}"
            if LOG_CHANNEL:
                send(LOG_CHANNEL, fwd_text)
            send(chat_id, "Terima kasih! ✨\nLaporan kamu sudah kami terima dan akan kami review.\n\n#jogjalend")
    return "ok", 200
