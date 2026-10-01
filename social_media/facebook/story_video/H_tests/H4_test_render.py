# ============================================================
# 📄 FILE:      H4_test_render.py
# 📁 PATH:      social_media/facebook/story_video/H_tests/H4_test_render.py
# 🎯 PURPOSE:   Render module import tests
# ============================================================


# ─────────────────────────────────────────────────────────────
# ① TEST: Frames class imports
# ─────────────────────────────────────────────────────────────
def test_frames_import():
    from D_video.D4_frames import Frames
    assert Frames is not None


# ─────────────────────────────────────────────────────────────
# ② TEST: Composer class imports
# ─────────────────────────────────────────────────────────────
def test_composer_import():
    from D_video.D6_composer import Composer
    assert Composer is not None


# ─────────────────────────────────────────────────────────────
# ③ TEST: FontLoader class imports
# ─────────────────────────────────────────────────────────────
def test_fonts_import():
    from B_graphics.B1_fonts import FontLoader
    assert FontLoader is not None
