# ============================================================
# FILE:      B4_progress_bar.py
# PATH:      social_media/facebook/story_video/B_graphics/B4_progress_bar.py
# PURPOSE:   Progress bar draw
# ============================================================

def draw_progress(draw, current, total, y=1820):
    bar_x, bar_w, bar_h = 80, 920, 8
    draw.rectangle([bar_x, y, bar_x + bar_w, y + bar_h], fill=(0, 0, 0, 150))
    pct = min(1.0, current / max(total, 1))
    fill_w = int(bar_w * pct)
    draw.rectangle([bar_x, y, bar_x + fill_w, y + bar_h],
                   fill=(212, 175, 55, 255))
    if fill_w > 0:
        gx = bar_x + fill_w
        draw.ellipse([gx - 8, y - 4, gx + 8, y + 12],
                     fill=(255, 220, 120, 220))
