# ============================================================
# 📄 FILE:      A2_logger.py
# 📁 PATH:      social_media/facebook/short_video/A_core/A2_logger.py
# 🎯 PURPOSE:   Print + Telegram logging (lazy imports)
# ============================================================

from datetime import datetime


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)


def log_file_start(name, purpose=""):
    log(f"→ START {name}")
    from A_core.A3_telegram import file_start
    file_start(name, purpose)


def log_file_end(name, status="success", note=""):
    log(f"← END {name} ({status})")
    from A_core.A3_telegram import file_end
    file_end(name, status, note)


def log_step(name, action, result="ok", detail=""):
    log(f"  • {name} :: {action} → {result} {detail}")
    from A_core.A3_telegram import step
    step(name, action, result, detail)


def log_api(name, api, status, detail=""):
    log(f"  ★ {name} :: {api} → {status}")
    from A_core.A3_telegram import api_call
    api_call(name, api, status, detail)


def log_error(name, error, tb=""):
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    from A_core.A3_telegram import file_error
    file_error(name, error, tb)
