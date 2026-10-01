# ============================================================
# FILE:      A4_utils.py
# PATH:      social_media/facebook/story_video/A_core/A4_utils.py
# PURPOSE:   Common helpers
# ============================================================

import os
import re


def sanitize(t):
    if not t:
        return ""
    t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path
