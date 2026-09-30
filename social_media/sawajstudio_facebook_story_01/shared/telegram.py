"""
Telegram notifications + global API status tracker.
"""
from shared.session import session
from shared.config import load_config

_config = load_config()

# Global API status dict — sab modules isme apna status likhte hain
api_status = {
    "AI": {},
    "TTS": {},
    "Music": {},
    "Background": {},
    "Translation": {},
    "Hadith": {},
    "Drive": {},
    "Facebook Story": {},
    "Instagram Story": {},
}


def send_tg(msg: str) -> None:
    """Send a Telegram message (HTML mode). Prints locally too."""
    print(msg)
    if _config.tg_token and _config.tg_chat_id:
        try:
            session.post(
                f"https://api.telegram.org/bot{_config.tg_token}/sendMessage",
                json={
                    "chat_id": _config.tg_chat_id,
                    "text": msg,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
                timeout=12,
            )
        except Exception:
            pass


def report_api_status() -> None:
    """Send a consolidated API status report to Telegram."""
    lines = ["📊 <b>API STATUS REPORT (Story)</b>\n"]
    for section, status in api_status.items():
        if not status:
            continue
        lines.append(f"<b>{section}:</b>")
        for name, result in status.items():
            if result == "success":
                icon = "✅"
            elif "failed" in str(result):
                icon = "❌"
            else:
                icon = "⏸️"
            lines.append(f"  {icon} {name} → {result}")
    send_tg("\n".join(lines))
