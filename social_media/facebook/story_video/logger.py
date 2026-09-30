"""Logger — prints + Telegram."""
from datetime import datetime
from telegram import (
    send_tg, file_start, file_end, step, file_error,
    api_call, header, summary,
)


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)


def log_file_start(name, purpose=""):
    log(f"→ START {name}")
    file_start(name, purpose)


def log_file_end(name, status="success", note=""):
    log(f"← END {name} ({status})")
    file_end(name, status, note)


def log_step(name, action, result="ok", detail=""):
    log(f"  • {name} :: {action} → {result} {detail}")
    step(name, action, result, detail)


def log_api(name, api, status, detail=""):
    log(f"  ★ {name} :: {api} → {status}")
    api_call(name, api, status, detail)


def log_error(name, error, tb=""):
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    file_error(name, error, tb)
