# ============================================================
# 📄 FILE:      H1_conftest.py
# 📁 PATH:      social_media/facebook/long_video/H_tests/H1_conftest.py
# 🎯 PURPOSE:   Pytest path setup
# ============================================================

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)
