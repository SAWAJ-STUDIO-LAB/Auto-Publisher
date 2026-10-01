# ============================================================
# FILE:      D5_transition.py
# PATH:      social_media/facebook/story_video/D_video/D5_transition.py
# PURPOSE:   Transition helpers
# ============================================================

def crossfade_alpha(current_t, start, duration):
    if current_t < start:
        return 0.0
    if current_t > start + duration:
        return 1.0
    return (current_t - start) / duration


def ease_in_out(x):
    return x * x * (3 - 2 * x)
