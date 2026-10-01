# ============================================================
# 📄 FILE:      H2_test_story.py
# 📁 PATH:      social_media/facebook/story_video/H_tests/H2_test_story.py
# 🎯 PURPOSE:   Basic tests for config + utils
# ============================================================

from A_core.A1_config import Config
from A_core.A4_utils import sanitize


# ─────────────────────────────────────────────────────────────
# ① TEST: Config class loads
# ─────────────────────────────────────────────────────────────
def test_config_import():
    """Config class should load."""
    assert Config is not None


# ─────────────────────────────────────────────────────────────
# ② TEST: Sanitize basic
# ─────────────────────────────────────────────────────────────
def test_sanitize_basic():
    assert sanitize("  hello\nworld  ") == "hello world"


# ─────────────────────────────────────────────────────────────
# ③ TEST: Sanitize quotes
# ─────────────────────────────────────────────────────────────
def test_sanitize_quotes():
    assert sanitize("it's a 'test'") == "its a test"


# ─────────────────────────────────────────────────────────────
# ④ TEST: Sanitize empty
# ─────────────────────────────────────────────────────────────
def test_sanitize_empty():
    assert sanitize("") == ""
    assert sanitize(None) == ""
