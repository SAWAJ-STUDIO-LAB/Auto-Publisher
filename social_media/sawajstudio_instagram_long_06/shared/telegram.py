import os, requests
from .session import get_session

session = get_session()
TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_tg(msg):
    if TG_TOKEN and TG_CHAT_ID:
        try:
            session.post(
                f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                json={"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True},
                timeout=12
            )
        except Exception as e:
            print(f"Telegram error: {e}")
    print(msg)
