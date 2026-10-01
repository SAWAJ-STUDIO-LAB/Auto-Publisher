
---

# 📁 FILE 5: `Makefile`

**Path:** `social_media/facebook/story_video/Makefile`

```makefile
# ============================================================
# 📄 FILE:      Makefile
# 📁 PATH:      social_media/facebook/story_video/Makefile
# 🎯 PURPOSE:   Short commands for common tasks
# ============================================================

.PHONY: install run test clean

# ─────────────────────────────────────────────────────────────
# ① INSTALL — install all dependencies
# ─────────────────────────────────────────────────────────────
install:
	pip install -r requirements.txt

# ─────────────────────────────────────────────────────────────
# ② RUN — run the full pipeline locally
# ─────────────────────────────────────────────────────────────
run:
	python3 G_entry/G2_run_story.py

# ─────────────────────────────────────────────────────────────
# ③ TEST — run all tests
# ─────────────────────────────────────────────────────────────
test:
	pytest -v

# ─────────────────────────────────────────────────────────────
# ④ CLEAN — remove temp files
# ─────────────────────────────────────────────────────────────
clean:
	rm -rf s_frames/ output/temp/* output/final/* *.mp3 *.mp4 avatar.png thumbnail.jpg __pycache__/ .pytest_cache/
