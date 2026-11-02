from flask import Flask, request
import os, requests, re
app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

def send(chat_id, text):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)

@app.route("/", methods=["GET","POST"])
def main():
    if request.method == "GET":
        return "JogLend Support OK", 200
    data = request.get_json(force=True, silent=True) or {}
    if "message" not in data:
        return "ok", 200
    msg = data["message"]
    chat_id = str(msg["chat"]["id"])
    text = msg.get("text","") or ""

    if chat_id == str(ADMIN_ID):
        if "reply_to_message" in msg and text:
            orig = msg["reply_to_message"].get("text","")
            m = re.search(r"ID:\s*(\d+)", orig)
            if m:
                target = m.group(1)
                send(target, f"💬 Balasan Admin:\n\n{text}")
                send(ADMIN_ID, f"✅ Terkirim ke {target}")
        return "ok", 200

    # user biasa
    if text.startswith("/start"):
        send(chat_id, "Support @menfessangel 📩\nKetik keluhan / saran kamu di sini, admin akan baca.")
    elif text:
        # UDAH DIHAPUS KATA SUPPORT BARU
        send(ADMIN_ID, f"Dari: {msg['from'].get('first_name')} (@{msg['from'].get('username','-')})\nID: {chat_id}\n\n{text}")
        send(chat_id, "Terima kasih! ✨ Laporan diterima dan akan kami review.")
    return "ok", 200
