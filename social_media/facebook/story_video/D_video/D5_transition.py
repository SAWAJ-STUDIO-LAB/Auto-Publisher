# ============================================================
# 📄 FILE:      D5_transition.py
# 📁 PATH:      social_media/facebook/story_video/D_video/D5_transition.py
# 🎯 PURPOSE:   Transition helpers (crossfade + easing)
# ============================================================

# ─────────────────────────────────────────────────────────────
# ① CROSSFADE ALPHA — smooth alpha 0 to 1
# ─────────────────────────────────────────────────────────────
def crossfade_alpha(current_t, start, duration):
    """Return alpha 0..1 for crossfade."""
    if current_t < start:
        return 0.0
    if current_t > start + duration:
        return 1.0
    return (current_t - start) / duration


# ─────────────────────────────────────────────────────────────
# ② EASE IN OUT — smooth easing function
# ─────────────────────────────────────────────────────────────
def ease_in_out(x):
    """Smooth easing function (S-curve)."""
    return x * x * (3 - 2 * x)
