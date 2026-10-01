# ============================================================
# 📄 FILE:      B1_fonts.py
# 📁 PATH:      social_media/facebook/short_video/B_graphics/B1_fonts.py
# 🎯 PURPOSE:   Font loader (Devanagari / Arabic / Latin)
# ============================================================

import os
from PIL import ImageFont


class FontLoader:
    """Load fonts from ~/.fonts/ with fallback."""

    @staticmethod
    def load(size, script="latin", bold=True):
        if script == "devanagari":
            paths = [
                "~/.fonts/NotoSansDevanagari-Bold.ttf" if bold
                else "~/.fonts/NotoSansDevanagari-Regular.ttf",
            ]
        elif script == "arabic":
            paths = [
                "~/.fonts/NotoNaskhArabic-Bold.ttf" if bold
                else "~/.fonts/NotoNaskhArabic-Regular.ttf",
            ]
        else:
            paths = [
                "~/.fonts/NotoSans-Bold.ttf" if bold
                else "~/.fonts/NotoSans-Regular.ttf",
            ]
        for p in paths:
            try:
                return ImageFont.truetype(os.path.expanduser(p), size)
            except Exception:
                continue
        return ImageFont.load_default()
