"""Utils."""
import os
import re
from logger import log_file_start, log_file_end, log_step


log_file_start("utils.py", "Sanitize + helpers")


def sanitize(t):
    if not t:
        return ""
    t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    log_step("utils.py", f"ensure_dir({path})", "ok")
    return path


log_file_end("utils.py", "success", "Helpers ready")
