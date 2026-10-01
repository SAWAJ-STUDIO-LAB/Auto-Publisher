# ============================================================
# 📄 FILE:      A4_utils.py
# 📁 PATH:      social_media/facebook/story_video/A_core/A4_utils.py
# 🎯 PURPOSE:   Common helper functions
# ============================================================

import os
import re


# ─────────────────────────────────────────────────────────────
# ① SANITIZE — clean text
# ─────────────────────────────────────────────────────────────
def sanitize(t):
    """
    Clean text:
      - Remove invisible unicode (zero-width, bidi)
      - Remove quotes
      - Remove newlines
      - Trim whitespace
    """
    if not t:
        return ""
    t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()


# ─────────────────────────────────────────────────────────────
# ② ENSURE DIR — create folder if missing
# ─────────────────────────────────────────────────────────────
def ensure_dir(path):
    """Create folder if not exists."""
    os.makedirs(path, exist_ok=True)
    return path
