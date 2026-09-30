
---

## 📁 File 5: `social_media/sawajstudio_facebook_story_01/Makefile`

```makefile
.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python -m runners.run_story

test:
	pytest tests/ -v

clean:
	rm -rf output/temp/* output/final/* __pycache__ .pytest_cache
	find . -name "*.mp3" -delete
	find . -name "*.mp4" -delete
	find . -name "*.ass" -delete
	find . -name "*.png" -delete
