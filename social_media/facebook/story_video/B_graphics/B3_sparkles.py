# ============================================================
# 📄 FILE:      B3_sparkles.py
# 📁 PATH:      social_media/facebook/story_video/B_graphics/B3_sparkles.py
# 🎯 PURPOSE:   Sparkle particles draw
# ============================================================

import math
import random


# ─────────────────────────────────────────────────────────────
# ① DRAW SPARKLES — floating golden sparkles
# ─────────────────────────────────────────────────────────────
def draw_sparkles(draw, t, count=12):
    """Draw floating sparkles."""
    rng = random.Random(int(t * 10))
    for _ in range(count):
        x = rng.randint(80, 1000)
        y = rng.randint(200, 1800)
        size = rng.randint(3, 9)
        alpha = int(120 + 100 * math.sin(t * 3 + x))
        alpha = max(50, min(255, alpha))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 240, 180, alpha))
