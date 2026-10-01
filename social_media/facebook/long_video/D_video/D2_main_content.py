# ============================================================
# 📄 FILE:      D2_main_content.py
# 📁 PATH:      social_media/facebook/long_video/D_video/D2_main_content.py
# 🎯 PURPOSE:   Main content (3-language word-by-word display)
# ============================================================

from B_graphics.B3_sparkles import draw_sparkles
from B_graphics.B4_progress_bar import draw_progress
from B_graphics.B5_badge import draw_badge
from B_graphics.B6_bullets import draw_bullets
from B_graphics.B7_watermark import draw_watermark, draw_floating_logo


def draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
              hadith_label, has_logo):
    alpha = min(1.0, mt / 0.5)

    if hadith_label:
        draw_badge(draw, hadith_label, y=180)

    if has_logo:
        draw_watermark(img, "avatar.png", size=(160, 68),
                       pos="top-right", opacity=0.55)
        draw_floating_logo(img, mt, "avatar.png", size=(240, 100))

    draw_bullets(draw, hindi, urdu, english, mt, voice_dur,
                 y_start=780, alpha=alpha)

    draw_progress(draw, mt, voice_dur)

    draw_sparkles(draw, mt)
