# ============================================================
# 📄 FILE:      D2_main_content.py
# 📁 PATH:      social_media/facebook/story_video/D_video/D2_main_content.py
# 🎯 PURPOSE:   Main content (3-language word-by-word display)
# ============================================================

from B_graphics.B3_sparkles import draw_sparkles
from B_graphics.B4_progress_bar import draw_progress
from B_graphics.B5_badge import draw_badge
from B_graphics.B6_bullets import draw_bullets
from B_graphics.B7_watermark import draw_watermark, draw_floating_logo


# ─────────────────────────────────────────────────────────────
# ① DRAW MAIN — draw main content frame
# ─────────────────────────────────────────────────────────────
def draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
              hadith_label, has_logo):
    """
    Draw main content frame.
    
    Args:
        mt: elapsed seconds in main content
        voice_dur: total voice duration
        hindi/urdu/english: text to display
        hadith_label: e.g. "#341 · Sahih al-Bukhari"
        has_logo: bool
    """
    alpha = min(1.0, mt / 0.5)

    # ───────── Hadith badge (top-left) ─────────
    if hadith_label:
        draw_badge(draw, hadith_label, y=180)

    # ───────── Watermark + floating logo ─────────
    if has_logo:
        # Small watermark (top-right, 55% opacity)
        draw_watermark(img, "avatar.png", size=(160, 68),
                       pos="top-right", opacity=0.55)
        # Floating logo (bottom-left, sine wave)
        draw_floating_logo(img, mt, "avatar.png", size=(240, 100))

    # ───────── 3-Language word-by-word bullets ─────────
    draw_bullets(draw, hindi, urdu, english, mt, voice_dur,
                 y_start=780, alpha=alpha)

    # ───────── Progress bar ─────────
    draw_progress(draw, mt, voice_dur)

    # ───────── Sparkles ─────────
    draw_sparkles(draw, mt)
