# ============================================================
# FILE:      H3_test_media.py
# PATH:      social_media/facebook/story_video/H_tests/H3_test_media.py
# PURPOSE:   Media module tests
# ============================================================

def test_music_import():
    from C_content.C5_music import Music
    assert Music is not None


def test_background_import():
    from C_content.C6_background import Background
    assert Background is not None


def test_tts_import():
    from C_content.C4_tts import TTS
    assert TTS is not None
