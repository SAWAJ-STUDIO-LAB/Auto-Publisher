# ============================================================
# FILE:      B6_bullets.py
# PATH:      social_media/facebook/story_video/B_graphics/B6_bullets.py
# PURPOSE:   3-language colored bullets
# ============================================================

from B_graphics.B1_fonts import FontLoader

C_HINDI = (240, 130, 200)
C_URDU = (90, 170, 255)
C_ENGLISH = (255, 110, 110)


def draw_bullets(draw, hindi, urdu, english, y_start=780, alpha=1.0):
    font_hindi = FontLoader.load(56, "devanagari", bold=True)
    font_arabic = FontLoader.load(56, "arabic", bold=True)
    font_latin = FontLoader.load(56, "latin", bold=True)

    y = y_start
    gap = 130

    if hindi:
        draw.ellipse([130, y + 22, 162, y + 54],
                     fill=(*C_HINDI, int(255 * alpha)))
        draw.text((193, y + 3), hindi,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_hindi)
        draw.text((190, y), hindi,
                  fill=(*C_HINDI, int(255 * alpha)), font=font_hindi)
        y += gap

    if urdu:
        draw.ellipse([130, y + 22, 162, y + 54],
                     fill=(*C_URDU, int(255 * alpha)))
        draw.text((193, y + 3), urdu,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_arabic)
        draw.text((190, y), urdu,
                  fill=(*C_URDU, int(255 * alpha)), font=font_arabic)
        y += gap

    if english:
        draw.ellipse([130, y + 22, 162, y + 54],
                     fill=(*C_ENGLISH, int(255 * alpha)))
        draw.text((193, y + 3), english,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_latin)
        draw.text((190, y), english,
                  fill=(*C_ENGLISH, int(255 * alpha)), font=font_latin)
