"""Compose final story video."""
import os
from logger import log_file_start, log_file_end, log_step


class Composer:
    def __init__(self, base):
        log_file_start("composer.py", "Final video composition")
        self.base = base
        log_file_end("composer.py", "success", "Ready")

    def compose(self, bg, frames_dir, voice, subs, total, outfile="Final_Story.mp4"):
        log_step("composer.py", "compose() starting", "ok",
                 f"total={total:.1f}s")
        fonts_dir = os.path.expanduser("~/.fonts")
        fps = 25
        self.base.run_cmd(
            f'ffmpeg -y -i {bg} -framerate {fps} -i {frames_dir}/frame_%05d.png -i {voice} '
            f'-filter_complex "[0:v][1:v]overlay=0:0:shortest=1,'
            f'subtitles={subs}:fontsdir={fonts_dir},'
            f'eq=contrast=1.08:brightness=0.02:saturation=1.12,vignette=PI/6,'
            f'format=yuv420p[outv]" '
            f'-map "[outv]" -map 2:a '
            f'-c:v libx264 -preset veryfast -crf 17 -b:v 7M '
            f'-c:a aac -b:a 192k -t {total:.2f} -movflags +faststart {outfile}')
        size_mb = os.path.getsize(outfile) / 1024 / 1024
        log_step("composer.py", f"Final video ready: {outfile}", "ok",
                 f"{size_mb:.1f} MB")
        return outfile
