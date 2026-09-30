"""
Facebook Story Video — Main Runner
"""
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    from telegram import send_tg, header, summary
    from logger import log_error

    header("🚀 FACEBOOK STORY RUNNER")
    send_tg("▶️ <b>Runner started</b>")
    try:
        from story_pipeline import StoryPipeline
        pipeline = StoryPipeline()
        pipeline.run()
        send_tg("🏁 <b>Runner exited cleanly</b>")
    except Exception as e:
        tb = traceback.format_exc()
        log_error("run_story.py", str(e), tb)
        send_tg(f"💥 <b>RUNNER FAILED</b>\n{str(e)[:200]}")
        summary()
        sys.exit(1)


if __name__ == "__main__":
    main()
