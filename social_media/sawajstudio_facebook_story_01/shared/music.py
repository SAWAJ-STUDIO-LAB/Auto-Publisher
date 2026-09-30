"""
Background music: Freesound → Pixabay CDN → generated sine.
Medium volume (0.22).
"""
import os
import random
from shared.session import session
from shared.telegram import api_status
from shared.utils import download, run_cmd
from shared.logger import get_logger

logger = get_logger("music")

MUSIC_VOL = 0.22


def get_music(target_dur: int = 110) -> str:
    """Download/generate soft background music. Returns filename."""
    fs = os.environ.get("FREESOUND_API_KEY")

    # 1) Try Freesound
    if fs:
        try:
            r = session.get(
                "https://freesound.org/apiv2/search/text/",
                params={
                    "query": "soft ambient meditation islamic peaceful",
                    "filter": "duration:[25 TO 160]",
                    "fields": "id,name,previews",
                    "page_size": 8,
                    "token": fs,
                },
                timeout=14,
            )
            if r.status_code == 200 and r.json().get("results"):
                s = random.choice(r.json()["results"])
                p = (
                    s.get("previews", {}).get("preview-hq-mp3")
                    or s.get("previews", {}).get("preview-lq-mp3")
                )
                if p and download(p, "music_raw.mp3"):
                    run_cmd(
                        f'ffmpeg -y -i music_raw.mp3 -af '
                        f'"volume={MUSIC_VOL},afade=t=in:st=0:d=2,afade=t=out:st=90:d=5" '
                        f"-t {target_dur} music_soft.mp3"
                    )
                    api_status["Music"]["Freesound"] = "success"
                    return "music_soft.mp3"
            api_status["Music"]["Freesound"] = "failed"
        except Exception as e:
            api_status["Music"]["Freesound"] = f"failed ({str(e)[:35]})"

    # 2) Pixabay CDN
    for u in [
        "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
        "https://cdn.pixabay.com/download/audio/2022/03/24/audio_4f3b5c5e3d.mp3?filename=peaceful-background-112194.mp3",
    ]:
        if download(u, "music_raw.mp3"):
            run_cmd(
                f'ffmpeg -y -i music_raw.mp3 -af '
                f'"volume={MUSIC_VOL},afade=t=in:st=0:d=2,afade=t=out:st=90:d=5" '
                f"-t {target_dur} music_soft.mp3"
            )
            api_status["Music"]["Pixabay-CDN"] = "success"
            return "music_soft.mp3"

    # 3) Generated sine fallback
    run_cmd(
        f'ffmpeg -y -f lavfi -i "sine=frequency=110:duration={target_dur}" '
        f'-af "afade=t=in:st=0:d=2.5,afade=t=out:st={target_dur - 10}:d=6,volume=0.12" '
        f"music_soft.mp3"
    )
    api_status["Music"]["Generated-Sine"] = "success (fallback)"
    return "music_soft.mp3"
