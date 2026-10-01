# ============================================================
# 📄 FILE:      B2_text_wrap.py
# 📁 PATH:      social_media/facebook/story_video/B_graphics/B2_text_wrap.py
# 🎯 PURPOSE:   Text wrap + center align helpers
# ============================================================

from PIL import ImageDraw, ImageFont


# ─────────────────────────────────────────────────────────────
# ① WRAP TEXT — split text into lines that fit max_width
# ─────────────────────────────────────────────────────────────
def wrap_text(draw, text, font, max_width=950):
    """Wrap text into lines that fit max_width."""
    if not text:
        return []
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


# ─────────────────────────────────────────────────────────────
# ② DRAW CENTERED — draw text centered at given y
# ─────────────────────────────────────────────────────────────
def draw_centered(draw, text, y, font, fill, shadow=True):
    """Draw text centered at given y with optional shadow."""
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (1080 - w) // 2
    if shadow:
        draw.text((x + 4, y + 4), text, fill=(0, 0, 0, 220), font=font)
    draw.text((x, y), text, fill=fill, font=font)


# ─────────────────────────────────────────────────────────────
# ③ DRAW LEFT — draw text left-aligned at given x,y
# ─────────────────────────────────────────────────────────────
def draw_left(draw, text, x, y, font, fill, shadow=True):
    """Draw text left-aligned at given x,y."""
    if not text:
        return
    if shadow:
        draw.text((x + 3, y + 3), text, fill=(0, 0, 0, 220), font=font)
    draw.text((x, y), text, fill=fill, font=font)
