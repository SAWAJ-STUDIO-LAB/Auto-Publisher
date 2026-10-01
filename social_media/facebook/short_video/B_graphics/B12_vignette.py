# ============================================================
# 📄 FILE:      B12_vignette.py
# 📁 PATH:      social_media/facebook/short_video/B_graphics/B12_vignette.py
# 🎯 PURPOSE:   Vignette (soft dark edges with pulse)
# ============================================================

import math


# ─────────────────────────────────────────────────────────────
# ① DRAW VIGNETTE — soft dark edges with breathing pulse
# ─────────────────────────────────────────────────────────────
def draw_vignette(draw, t, intensity=60):
    """Draw vignette (breathing effect)."""
    pulse = int(intensity + 20 * math.sin(t * 0.8))
    pulse = max(20, min(100, pulse))

    edges = [
        (0, 0, 1080, 200),
        (0, 1720, 1080, 1920),
        (0, 0, 150, 1920),
        (930, 0, 1080, 1920),
    ]
    for (x1, y1, x2, y2) in edges:
        draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, pulse))
