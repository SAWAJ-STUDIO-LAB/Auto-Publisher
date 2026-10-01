# ============================================================
# FILE:      B5_badge.py
# PATH:      social_media/facebook/story_video/B_graphics/B5_badge.py
# PURPOSE:   Hadith badge draw
# ============================================================

from B_graphics.B1_fonts import FontLoader


def draw_badge(draw, text, y=180):
    if not text:
        return
    fnt = FontLoader.load(26, "latin", bold=True)
    bbox = draw.textbbox((0, 0), text, font=fnt)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    pad = 12
    x1, y1 = 60, y
    x2, y2 = x1 + w + pad * 2, y1 + h + pad
    draw.rounded_rectangle([x1, y1, x2, y2], radius=8,
                           fill=(20, 15, 8, 200),
                           outline=(212, 175, 55, 220), width=2)
    draw.text((x1 + pad, y1 + pad // 2), text,
              fill=(230, 200, 130, 255), font=fnt)
