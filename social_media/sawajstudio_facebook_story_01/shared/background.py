"""
Background video: Pexels → Pixabay → generated gradient.
"""
import os
import random
from shared.session import session
from shared.telegram import api_status
from shared.utils import download, run_cmd
from shared.logger import get_logger

logger = get_logger("background")

DARKEN = "eq=contrast=1.10:brightness=0.02:saturation=1.12,vignette=PI/5"
QUERIES = [
    "islamic architecture night",
    "mosque night",
    "night sky stars",
    "desert night",
    "kaaba night",
]


def get_bg(dur: float) -> str:
    """Return path to a 1080x1920 background video of given duration."""
    out = "bg.mp4"

    # 1) Pexels
    pk = os.environ.get("PEXELS_API_KEY")
    if pk:
        for q in random.sample(QUERIES, 4):
            try:
                r = session.get(
                    f"https://api.pexels.com/videos/search?query={q}"
                    f"&orientation=portrait&per_page=6",
                    headers={"Authorization": pk},
                    timeout=14,
                )
                if r.status_code == 200 and r.json().get("videos"):
                    v = random.choice(r.json()["videos"])
                    files = sorted(
                        v.get("video_files", []),
                        key=lambda x: x.get("width", 0),
                        reverse=True,
                    )
                    if files and download(files[0]["link"], "tmp.mp4"):
                        run_cmd(_ffmpeg_bg_cmd(dur, out))
                        api_status["Background"]["Pexels"] = "success"
                        return out
            except Exception:
                pass
        api_status["Background"]["Pexels"] = "failed"

    # 2) Pixabay
    px = os.environ.get("PIXABAY_API_KEY")
    if px:
        try:
            r = session.get(
                f"https://pixabay.com/api/videos/?key={px}"
                f"&q=mosque+night&orientation=vertical&per_page=8",
                timeout=14,
            )
            if r.status_code == 200 and r.json().get("hits"):
                h = random.choice(r.json()["hits"])
                u = (
                    h.get("videos", {}).get("large", {}).get("url")
                    or h.get("videos", {}).get("medium", {}).get("url")
                )
                if u and download(u, "tmp.mp4"):
                    run_cmd(_ffmpeg_bg_cmd(dur, out))
                    api_status["Background"]["Pixabay"] = "success"
                    return out
            api_status["Background"]["Pixabay"] = "failed"
        except Exception as e:
            api_status["Background"]["Pixabay"] = f"failed ({str(e)[:35]})"

    # 3) Generated gradient
    c0 = f"{random.randint(10, 30):02x}{random.randint(8, 25):02x}{random.randint(25, 55):02x}"
    c1 = f"{random.randint(10, 30):02x}{random.randint(8, 25):02x}{random.randint(25, 55):02x}"
    run_cmd(
        f'ffmpeg -y -f lavfi -i "gradients=s=1080x1920:c0=0x{c0}:c1=0x{c1}:speed=0.006" '
        f"-t {dur:.2f} -c:v libx264 -preset veryfast {out}"
    )
    api_status["Background"]["Generated-Gradient"] = "success (fallback)"
    return out


def _ffmpeg_bg_cmd(dur: float, out: str) -> str:
    """Build the ffmpeg command for scaling/cropping/zooming."""
    return (
        f'ffmpeg -y -stream_loop -1 -i tmp.mp4 -vf '
        f'"scale=1200:2140:force_original_aspect_ratio=increase,'
        f'crop=1080:1920,'
        f"zoompan=z='min(zoom+0.0004,1.06)':d=1:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,"
        f'setsar=1,{DARKEN}" '
        f"-t {dur:.2f} -an -c:v libx264 -preset veryfast -crf 18 {out}"
    )
