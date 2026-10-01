# ============================================================
# FILE:      B2_text_wrap.py
# PATH:      social_media/facebook/story_video/B_graphics/B2_text_wrap.py
# PURPOSE:   Text wrap + center align
# ============================================================

def wrap_text(draw, text, font, max_width=950):
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


def draw_centered(draw, text, y, font, fill, shadow=True):
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (1080 - w) // 2
    if shadow:
        draw.text((x + 4, y + 4), text, fill=(0, 0, 0, 220), font=font)
    draw.text((x, y), text, fill=fill, font=font)
