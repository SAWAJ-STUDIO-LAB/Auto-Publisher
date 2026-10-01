# ============================================================
# 📄 FILE:      A4_utils.py
# 📁 PATH:      social_media/facebook/short_video/A_core/A4_utils.py
# 🎯 PURPOSE:   Common helper functions
# ============================================================

import os
import re


def sanitize(t):
    """Clean text — remove invisible unicode, quotes, newlines."""
    if not t:
        return ""
    t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()


def ensure_dir(path):
    """Create folder if not exists."""
    os.makedirs(path, exist_ok=True)
    return path
