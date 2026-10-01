# ============================================================
# 📄 FILE:      D1_intro.py
# 📁 PATH:      social_media/facebook/long_video/D_video/D1_intro.py
# 🎯 PURPOSE:   Intro frames (Bismillah + Logo + Title)
# ⏱️  TIMING:   Intro = 2 seconds
# ============================================================

import os
from PIL import Image
from B_graphics.B1_fonts import FontLoader
from B_graphics.B2_text_wrap import draw_centered
from B_graphics.B3_sparkles import draw_sparkles


def draw_intro(img, draw, t, intro_dur, has_logo):
    p = t / intro_dur
    alpha = min(1.0, t / 0.5)

    font_arabic = FontLoader.load(56, "arabic", bold=True)
    font_title = FontLoader.load(76, "latin", bold=True)
    font_sub = FontLoader.load(40, "latin", bold=False)

    C_GOLD = (230, 200, 130)

    draw_centered(draw, "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ",
                  200, font_arabic, (*C_GOLD, int(255 * alpha)))

    line_y = 320
    line_progress = min(1.0, max(0.0, (p - 0.2) / 0.4))
    if line_progress > 0:
        lw = int(600 * line_progress)
        lx = (1080 - lw) // 2
        draw.rectangle([lx, line_y, lx + lw, line_y + 3],
                       fill=(*C_GOLD, int(255 * line_progress)))

    if has_logo:
        logo_p = min(1.0, max(0.0, (p - 0.3) / 0.4))
        if logo_p > 0:
            try:
                base = Image.open("avatar.png").convert("RGBA")
                sw = int(240 * (0.6 + 0.4 * logo_p))
                sh = int(100 * (0.6 + 0.4 * logo_p))
