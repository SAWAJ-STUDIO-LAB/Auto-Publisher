# ============================================================
# 📄 FILE:      H2_test_long.py
# 📁 PATH:      social_media/facebook/long_video/H_tests/H2_test_long.py
# 🎯 PURPOSE:   Basic tests
# ============================================================

from A_core.A1_config import Config
from A_core.A4_utils import sanitize


def test_config_import():
    assert Config is not None


def test_sanitize_basic():
    assert sanitize("  hello\nworld  ") == "hello world"


def test_sanitize_quotes():
    assert sanitize("it's a 'test'") == "its a test"


def test_sanitize_empty():
    assert sanitize("") == ""
    assert sanitize(None) == ""
