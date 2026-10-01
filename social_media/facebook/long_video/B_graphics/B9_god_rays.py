# ============================================================
# 📄 FILE:      B9_god_rays.py
# 📁 PATH:      social_media/facebook/long_video/B_graphics/B9_god_rays.py
# 🎯 PURPOSE:   Light rays from top
# ============================================================

import math


def draw_god_rays(draw, t, opacity=25):
    """Draw soft light beams from top center."""
    cx = 540
    for i in range(5):
        angle = -math.pi / 2 + (i - 2) * 0.15 + 0.02 * math.sin(t)
        length = 800
        x2 = cx + int(length * math.cos(angle))
        y2 = int(length * math.sin(angle))
        draw.line([(cx, 0), (x2, y2)],
                  fill=(255, 240, 180, opacity), width=40)
