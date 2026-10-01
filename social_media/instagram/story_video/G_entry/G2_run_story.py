# ============================================================
# FILE:      G2_run_story.py
# PATH:      social_media/facebook/story_video/G_entry/G2_run_story.py
# PURPOSE:   Entry point
# ============================================================

import os
import sys
import traceback

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)


def main():
    from A_core.A3_telegram import run_start, send_full_report, send_summary
    from A_core.A2_logger import log_error

    run_start("📘 FACEBOOK STORY RUN")

    try:
        from G_entry.G1_story_pipeline import StoryPipeline
        pipeline = StoryPipeline()
        pipeline.run()
        send_full_report()
        send_summary()
    except Exception as e:
        tb = traceback.format_exc()
        log_error("G2_run_story.py", str(e), tb)
        send_full_report()
        send_summary()
        sys.exit(1)


if __name__ == "__main__":
    main()
