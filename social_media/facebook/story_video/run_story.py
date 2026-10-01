"""
Facebook Story Video — Main Runner
"""
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    from telegram import run_start, send_full_report, send_summary
    from logger import log_error

    run_start("📘 FACEBOOK STORY RUN")

    try:
        from story_pipeline import StoryPipeline
        pipeline = StoryPipeline()
        pipeline.run()
        send_full_report()
        send_summary()
    except Exception as e:
        tb = traceback.format_exc()
        log_error("run_story.py", str(e), tb)
        send_full_report()
        send_summary()
        sys.exit(1)


if __name__ == "__main__":
    main()
