# ============================================================
# 📄 FILE:      A3_telegram.py
# 📁 PATH:      social_media/facebook/story_video/A_core/A3_telegram.py
# 🎯 PURPOSE:   Combined Telegram report — buffer + send
# ⚠️  NOTE:     Uses env vars directly (circular-safe)
# ============================================================

import os
import time
import requests
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# ① HTTP SESSION (reused for all Telegram calls)
# ─────────────────────────────────────────────────────────────
_session = requests.Session()


# ─────────────────────────────────────────────────────────────
# ② GLOBAL BUFFERS
# ─────────────────────────────────────────────────────────────
LOG_BUFFER = []          # All log lines to send at end
FILE_TIMERS = {}         # Track time per file
FILE_RESULTS = []        # (filename, status, elapsed, note)
STEP_COUNTER = {"total": 0, "success": 0, "failed": 0}
START_TIME = None
RUN_HEADER = "📘 FACEBOOK STORY RUN"


# ─────────────────────────────────────────────────────────────
# ③ HELPERS
# ─────────────────────────────────────────────────────────────
def _now():
    """Current time HH:MM:SS."""
    return datetime.now().strftime("%H:%M:%S")


def _creds():
    """Get Telegram credentials from env."""
    return os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")


def _send_raw(msg, silent=False):
    """Send message to Telegram (max 4000 chars)."""
    token, chat_id = _creds()
    if token and chat_id:
        try:
            _session.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": msg[:4000],
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "disable_notification": silent,
                },
                timeout=15,
            )
        except Exception:
            pass
    print(msg, flush=True)


# ─────────────────────────────────────────────────────────────
# ④ RUN START — called once at very beginning
# ─────────────────────────────────────────────────────────────
def run_start(title="📘 FACEBOOK STORY RUN"):
    """Initialize run — resets all buffers."""
    global START_TIME, RUN_HEADER, LOG_BUFFER
    START_TIME = time.time()
    RUN_HEADER = title
    LOG_BUFFER = []
    FILE_RESULTS.clear()
    STEP_COUNTER.update({"total": 0, "success": 0, "failed": 0})
    _send_raw(f"▶️ <b>{title} STARTED</b>\n🕐 {_now()}", silent=True)


# ─────────────────────────────────────────────────────────────
# ⑤ FILE START — called at start of each module
# ─────────────────────────────────────────────────────────────
def file_start(filename, purpose=""):
    """Log start of a module (adds to buffer)."""
    FILE_TIMERS[filename] = time.time()
    STEP_COUNTER["total"] += 1
    line = f"📂 <b>{filename}</b>"
    if purpose:
        line += f" — <i>{purpose}</i>"
    LOG_BUFFER.append(line)


# ─────────────────────────────────────────────────────────────
# ⑥ FILE END — called at end of each module
# ─────────────────────────────────────────────────────────────
def file_end(filename, status="success", note=""):
    """Log end of a module (adds to buffer)."""
    elapsed = time.time() - FILE_TIMERS.get(filename, time.time())
    if status == "success":
        STEP_COUNTER["success"] += 1
        icon = "✅"
    else:
        STEP_COUNTER["failed"] += 1
        icon = "❌"
    FILE_RESULTS.append((filename, status, elapsed, note))
    line = f"{icon} <b>{filename}</b> done in {elapsed:.2f}s"
    if note:
        line += f" — {note}"
    LOG_BUFFER.append(line)


# ─────────────────────────────────────────────────────────────
# ⑦ STEP — called for each step
# ─────────────────────────────────────────────────────────────
def step(filename, action, result="ok", detail=""):
    """Log a step (adds to buffer)."""
    icon = {
        "ok": "✅", "fail": "❌", "skip": "⏭️",
        "warn": "⚠️", "info": "ℹ️",
    }.get(result, "ℹ️")
    line = f"{icon} <b>{filename}</b> → {action}"
    if detail:
        line += f" ({detail})"
    LOG_BUFFER.append(line)


# ─────────────────────────────────────────────────────────────
# ⑧ API CALL — called for each external API
# ─────────────────────────────────────────────────────────────
def api_call(filename, api_name, status, detail=""):
    """Log an API call (adds to buffer)."""
    icon = {
        "success": "🟢", "failed": "🔴",
        "fallback": "🟡", "skipped": "⚪",
    }.get(status, "⚫")
    line = f"{icon} <b>{api_name}</b> [{status.upper()}]"
    if detail:
        line += f" — {detail}"
    LOG_BUFFER.append(line)


# ─────────────────────────────────────────────────────────────
# ⑨ ERROR — called when error occurs
# ─────────────────────────────────────────────────────────────
def file_error(filename, error, tb=""):
    """Log error (adds to buffer)."""
    STEP_COUNTER["failed"] += 1
    line = f"🚨 <b>{filename}</b> ERROR: {str(error)[:150]}"
    if tb:
        line += f"\n<code>{tb[:200]}</code>"
    LOG_BUFFER.append(line)


# ─────────────────────────────────────────────────────────────
# ⑩ HEADER — big section header
# ─────────────────────────────────────────────────────────────
def header(title):
    """Add a section header to buffer."""
    LOG_BUFFER.append(f"\n<b>━━━ {title} ━━━</b>")


# ─────────────────────────────────────────────────────────────
# ⑪ DIRECT SEND — send message immediately
# ─────────────────────────────────────────────────────────────
def send_tg(msg, silent=False):
    """Send message to Telegram immediately."""
    _send_raw(msg, silent=silent)


# ─────────────────────────────────────────────────────────────
# ⑫ FULL REPORT — send entire buffer (auto-split)
# ─────────────────────────────────────────────────────────────
def send_full_report(extra_sections=None, silent=False):
    """Send all buffered logs as Telegram message(s)."""
    total_time = time.time() - (START_TIME or time.time())
    head = (
        f"<b>{RUN_HEADER} — FULL REPORT</b>\n"
        f"🕐 {_now()}  |  ⏱️ {total_time:.1f}s\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    )
    body = "\n".join(LOG_BUFFER)
    extras = ""
    if extra_sections:
        extras = "\n\n" + "\n".join(extra_sections)
    full = head + body + extras

    # Auto-split at 3800 chars
    chunks = []
    current = ""
    for line in full.split("\n"):
        if len(current) + len(line) + 1 > 3800:
            chunks.append(current)
            current = line
        else:
            current += ("\n" if current else "") + line
    if current:
        chunks.append(current)

    for i, chunk in enumerate(chunks, 1):
        prefix = f"📄 <b>Report {i}/{len(chunks)}</b>\n" if len(chunks) > 1 else ""
        _send_raw(prefix + chunk, silent=silent)


# ─────────────────────────────────────────────────────────────
# ⑬ SUMMARY — send final summary message
# ─────────────────────────────────────────────────────────────
def send_summary(silent=False):
    """Send final summary message."""
    total = STEP_COUNTER["total"]
    ok = STEP_COUNTER["success"]
    fail = STEP_COUNTER["failed"]
    total_time = time.time() - (START_TIME or time.time())
    icon = "🎉" if fail == 0 else "⚠️"
    msg = (
        f"{icon} <b>RUN COMPLETE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📁 Files processed: <b>{total}</b>\n"
        f"✅ Success: <b>{ok}</b>\n"
        f"❌ Failed: <b>{fail}</b>\n"
        f"⏱️ Total time: <b>{total_time:.1f}s</b>\n"
        f"🕐 Finished: <b>{_now()}</b>"
    )
    _send_raw(msg, silent=silent)


def summary():
    """Alias for send_summary."""
    send_summary()
