"""Telegram notifier — detailed step-by-step logging."""
import time
import requests
from datetime import datetime
from config import Config

_session = requests.Session()

FILE_TIMERS = {}
STEP_COUNTER = {"total": 0, "success": 0, "failed": 0}


def _now():
    return datetime.now().strftime("%H:%M:%S")


def send_tg(msg, silent=False):
    if Config.TG_TOKEN and Config.TG_CHAT_ID:
        try:
            _session.post(
                f"https://api.telegram.org/bot{Config.TG_TOKEN}/sendMessage",
                json={
                    "chat_id": Config.TG_CHAT_ID,
                    "text": msg,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "disable_notification": silent,
                },
                timeout=12,
            )
        except Exception:
            pass
    print(msg, flush=True)


def file_start(filename, purpose=""):
    FILE_TIMERS[filename] = time.time()
    STEP_COUNTER["total"] += 1
    msg = f"📂 <b>FILE START</b>\n├─ <code>{filename}</code>"
    if purpose:
        msg += f"\n└─ 🎯 {purpose}"
    send_tg(msg, silent=True)


def file_end(filename, status="success", note=""):
    elapsed = time.time() - FILE_TIMERS.get(filename, time.time())
    if status == "success":
        STEP_COUNTER["success"] += 1
        icon, head = "✅", "FILE DONE"
    else:
        STEP_COUNTER["failed"] += 1
        icon, head = "❌", "FILE FAILED"
    msg = f"{icon} <b>{head}</b>\n├─ <code>{filename}</code>\n├─ ⏱️ {elapsed:.2f}s"
    if note:
        msg += f"\n└─ 📝 {note}"
    send_tg(msg, silent=True)


def step(filename, action, result="ok", detail="", silent=True):
    icon = {
        "ok": "  ✅", "fail": "  ❌", "skip": "  ⏭️",
        "warn": "  ⚠️", "info": "  ℹ️",
    }.get(result, "  ℹ️")
    msg = f"{icon} <code>{filename}</code> → <b>{action}</b>"
    if detail:
        msg += f"\n      └─ {detail}"
    send_tg(msg, silent=silent)


def api_call(filename, api_name, status, detail="", silent=True):
    icon = {
        "success": "🟢", "failed": "🔴",
        "fallback": "🟡", "skipped": "⚪",
    }.get(status, "⚫")
    msg = f"{icon} <code>{filename}</code> → <b>{api_name}</b>: {status.upper()}"
    if detail:
        msg += f"\n   └─ {detail}"
    send_tg(msg, silent=silent)


def file_error(filename, error, tb=""):
    STEP_COUNTER["failed"] += 1
    msg = (f"🚨 <b>ERROR in</b> <code>{filename}</code>\n"
           f"├─ 💬 {str(error)[:200]}")
    if tb:
        msg += f"\n└─ 📜 <code>{tb[:300]}</code>"
    send_tg(msg, silent=False)


def header(title):
    send_tg(f"\n{'━' * 20}\n<b>{title}</b>\n{'━' * 20}", silent=True)


def summary():
    total = STEP_COUNTER["total"]
    ok = STEP_COUNTER["success"]
    fail = STEP_COUNTER["failed"]
    msg = (f"📊 <b>FINAL SUMMARY</b>\n"
           f"├─ 📁 Files processed: {total}\n"
           f"├─ ✅ Success: {ok}\n"
           f"├─ ❌ Failed: {fail}\n"
           f"└─ 🕐 Finished: {_now()}")
    send_tg(msg, silent=False)
