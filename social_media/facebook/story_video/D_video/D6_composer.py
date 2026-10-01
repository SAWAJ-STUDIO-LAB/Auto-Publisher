# ============================================================
# 📄 FILE:      D6_composer.py
# 📁 PATH:      social_media/facebook/story_video/D_video/D6_composer.py
# 🎯 PURPOSE:   Compose final video from frames + audio
# ============================================================

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step


# ─────────────────────────────────────────────────────────────
# ① COMPOSER CLASS
# ─────────────────────────────────────────────────────────────
class Composer:
    """Final video composer using FFmpeg."""

    # ─────────────────────────────────────────────────────────
    # ② INIT
    # ─────────────────────────────────────────────────────────
    def __init__(self, base):
        log_file_start("D6_composer.py", "Final video composition")
        self.base = base
        log_file_end("D6_composer.py", "success", "Ready")

    # ─────────────────────────────────────────────────────────
    # ③ COMPOSE — compose final video
    # ─────────────────────────────────────────────────────────
    def compose(self, bg, frames_dir, voice, total,
                outfile="output/final/Final_Story.mp4"):
        log_step("D6_composer.py", "compose() starting", "ok",
                 f"total={total:.1f}s")

        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        fps = 25

        self.base.run_cmd(
            f'ffmpeg -y -i {bg} -framerate {fps} '
            f'-i {frames_dir}/frame_%05d.png '
            f'-i {voice} '
            f'-filter_complex "[0:v][1:v]overlay=0:0:shortest=1,'
            f'eq=contrast=1.08:brightness=0.02:saturation=1.12,vignette=PI/6,'
            f'format=yuv420p[outv]" '
            f'-map "[outv]" -map 2:a '
            f'-c:v libx264 -preset veryfast -crf 17 -b:v 7M '
            f'-c:a aac -b:a 192k -t {total:.2f} -movflags +faststart {outfile}')

        size_mb = os.path.getsize(outfile) /
