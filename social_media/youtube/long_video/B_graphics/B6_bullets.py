# ============================================================
# FILE:      B6_bullets.py
# PATH:      social_media/facebook/story_video/B_graphics/B6_bullets.py
# PURPOSE:   Word-by-word 3-language bullets (AI speaking style)
# NOTE:      Only ONE word per language at a time
#            Auto-speed so all languages finish in same time
# ============================================================

from B_graphics.B1_fonts import FontLoader


# ----- Bullet colors -----
C_HINDI = (240, 130, 200)      # Pink
C_URDU = (90, 170, 255)        # Blue
C_ENGLISH = (255, 110, 110)    # Red


def _current_word(text, elapsed, total_dur):
    """
    Return ONLY the current word based on elapsed time.
    
    Auto-calculates speed so the LAST word is reached exactly
    at total_dur (all languages finish at same time).
    
    Args:
        text: full text (Hindi / Arabic / English)
        elapsed: seconds passed in main content
        total_dur: total voice duration
    
    Returns:
        Current single word (str)
    """
    if not text:
        return ""

    words = text.split()
    if not words:
        return ""

    # Auto speed: all words finish in total_dur seconds
    word_speed = max(0.25, total_dur / max(len(words), 1))

    idx = int(elapsed / word_speed)
    if idx >= len(words):
        idx = len(words) - 1

    return words[idx]


def draw_bullets(draw, hindi, urdu, english, elapsed, voice_dur,
                 y_start=780, alpha=1.0):
    """
    Draw 3-language bullets — ONLY CURRENT WORD per language.
    
    Layout:
        🟣 (Hindi word)
        🔵 (Arabic word)
        🔴 (English word)
    
    Each word changes every ~0.4 seconds.
    """
    # Bigger fonts (72) — because only 1 word shows
    font_hindi = FontLoader.load(72, "devanagari", bold=True)
    font_arabic = FontLoader.load(72, "arabic", bold=True)
    font_latin = FontLoader.load(72, "latin", bold=True)

    y = y_start
    gap = 180

    # Get current word for each language
    cur_hindi = _current_word(hindi, elapsed, voice_dur)
    cur_urdu = _current_word(urdu, elapsed, voice_dur)
    cur_english = _current_word(english, elapsed, voice_dur)

    # ---------- HINDI (Pink) ----------
    if cur_hindi:
        # Bullet circle
        draw.ellipse([130, y + 30, 170, y + 70],
                     fill=(*C_HINDI, int(255 * alpha)))
        # Text shadow
        draw.text((196, y + 4), cur_hindi,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_hindi)
        # Text main
        draw.text((190, y), cur_hindi,
                  fill=(*C_HINDI, int(255 * alpha)), font=font_hindi)
    y += gap

    # ---------- URDU / ARABIC (Blue) ----------
    if cur_urdu:
        draw.ellipse([130, y + 30, 170, y + 70],
                     fill=(*C_URDU, int(255 * alpha)))
        draw.text((196, y + 4), cur_urdu,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_arabic)
        draw.text((190, y), cur_urdu,
                  fill=(*C_URDU, int(255 * alpha)), font=font_arabic)
    y += gap

    # ---------- ENGLISH (Red) ----------
    if cur_english:
        draw.ellipse([130, y + 30, 170, y + 70],
                     fill=(*C_ENGLISH, int(255 * alpha)))
        draw.text((196, y + 4), cur_english,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_latin)
        draw.text((190, y), cur_english,
                  fill=(*C_ENGLISH, int(255 * alpha)), font=font_latin)
