
---

# 📁 FILE 5: `Makefile`

**Path:** `social_media/facebook/short_video/Makefile`

```makefile
# ============================================================
# 📄 FILE:      Makefile
# 📁 PATH:      social_media/facebook/short_video/Makefile
# 🎯 PURPOSE:   Short commands
# ============================================================

.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python3 G_entry/G2_run_short.py

test:
	pytest -v

clean:
	rm -rf p_frames/ output/temp/* output/final/* *.mp3 *.mp4 avatar.png thumbnail.jpg __pycache__/ .pytest_cache/
