"""
Final video composer — overlays frames on background,
burns subtitles, adds voice audio.
"""
import os
from shared.utils import run_cmd
from shared.logger import get_logger

logger = get_logger("composer")

FPS = 25


def compose_story_video(
    bg: str,
    frames_dir: str,
    voice: str,
    subs: str,
    total: float,
    outfile: str = "Final_Story.mp4",
) -> str:
    """Compose final video. Returns outfile path."""
    fonts_dir = os.path.expanduser("~/.fonts")

    cmd = (
        f'ffmpeg -y -i {bg} -framerate {FPS} -i {frames_dir}/frame_%05d.png -i {voice} '
        f'-filter_complex "[0:v][1:v]overlay=0:0:shortest=1,'
        f'subtitles={subs}:fontsdir={fonts_dir},'
        f'eq=contrast=1.08:brightness=0.02:saturation=1.12,vignette=PI/6,'
        f'format=yuv420p[outv]" '
        f'-map "[outv]" -map 2:a '
        f"-c:v libx264 -preset veryfast -crf 17 -b:v 7M "
        f"-c:a aac -b:a 192k -t {total:.2f} -movflags +faststart {outfile}"
    )
    run_cmd(cmd)
    logger.info(f"Final video → {outfile}")
    return outfile
