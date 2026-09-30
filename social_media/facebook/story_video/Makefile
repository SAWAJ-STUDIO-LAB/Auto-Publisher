.PHONY: run test clean install

install:
	pip install -r requirements.txt

run:
	python3 run_story.py

test:
	pytest -v

clean:
	rm -rf s_frames/ *.mp3 *.mp4 avatar.png __pycache__/ .pytest_cache/
