# ============================================================
# 📄 FILE:      A2_logger.py
# 📁 PATH:      social_media/facebook/story_video/A_core/A2_logger.py
# 🎯 PURPOSE:   Print + Telegram logging (lazy imports)
# ⚠️  NOTE:     Lazy imports to avoid circular dependency
# ============================================================

from datetime import datetime


# ─────────────────────────────────────────────────────────────
# ① BASIC PRINT LOGGER
# ─────────────────────────────────────────────────────────────
def log(msg, level="INFO"):
    """
    Print message with timestamp.
    
    Args:
        msg: message to log
        level: INFO / WARNING / ERROR
    """
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)


# ─────────────────────────────────────────────────────────────
# ② FILE START — called at beginning of module
# ─────────────────────────────────────────────────────────────
def log_file_start(name, purpose=""):
    """Log start of a module."""
    log(f"→ START {name}")
    from A_core.A3_telegram import file_start
    file_start(name, purpose)


# ─────────────────────────────────────────────────────────────
# ③ FILE END — called at end of module
# ─────────────────────────────────────────────────────────────
def log_file_end(name, status="success", note=""):
    """Log end of a module."""
    log(f"← END {name} ({status})")
    from A_core.A3_telegram import file_end
    file_end(name, status, note)


# ─────────────────────────────────────────────────────────────
# ④ STEP — called for each step inside module
# ─────────────────────────────────────────────────────────────
def log_step(name, action, result="ok", detail=""):
    """Log a specific step."""
    log(f"  • {name} :: {action} → {result} {detail}")
    from A_core.A3_telegram import step
    step(name, action, result, detail)


# ─────────────────────────────────────────────────────────────
# ⑤ API CALL — called for each external API call
# ─────────────────────────────────────────────────────────────
def log_api(name, api, status, detail=""):
    """Log an API call result."""
    log(f"  ★ {name} :: {api} → {status}")
    from A_core.A3_telegram import api_call
    api_call(name, api, status, detail)


# ─────────────────────────────────────────────────────────────
# ⑥ ERROR — called when an error occurs
# ─────────────────────────────────────────────────────────────
def log_error(name, error, tb=""):
    """Log an error with optional traceback."""
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    from A_core.A3_telegram import file_error
    file_error(name, error, tb)
