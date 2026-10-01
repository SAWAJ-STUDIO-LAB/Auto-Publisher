# ============================================================
# 📄 FILE:      H4_test_render.py
# 📁 PATH:      social_media/facebook/short_video/H_tests/H4_test_render.py
# 🎯 PURPOSE:   Render module import tests
# ============================================================


def test_frames_import():
    from D_video.D4_frames import Frames
    assert Frames is not None


def test_composer_import():
    from D_video.D6_composer import Composer
    assert Composer is not None


def test_fonts_import():
    from B_graphics.B1_fonts import FontLoader
    assert FontLoader is not None
