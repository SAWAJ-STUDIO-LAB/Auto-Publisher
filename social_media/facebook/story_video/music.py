"""Background music — Freesound → Pixabay → generated fallback."""
import os
import random
from logger import log_file_start, log_file_end, log_step, log_api


MUSIC_VOL = 0.22


class Music:
    def __init__(self, base):
        log_file_start("music.py", "Background music fetch")
        self.base = base
        log_file_end("music.py", "success", "Ready")

    def get(self, outfile="music_soft.mp3"):
        log_step("music.py", "get() starting", "ok")

        fs = os.environ.get("FREESOUND_API_KEY")
        if fs:
            try:
                log_step("music.py", "Trying Freesound", "info")
                r = self.base.session.get(
                    "https://freesound.org/apiv2/search/text/",
                    params={
                        "query": "soft ambient meditation islamic peaceful",
                        "filter": "duration:[25 TO 160]",
                        "fields": "id,name,previews",
                        "page_size": 8, "token": fs,
                    }, timeout=14)
                if r.status_code == 200 and r.json().get("results"):
                    s = random.choice(r.json()["results"])
                    p = (s.get("previews", {}).get("preview-hq-mp3")
                         or s.get("previews", {}).get("preview-lq-mp3"))
                    if p and self.base.download(p, "music_raw.mp3"):
                        self.base.run_cmd(
                            f'ffmpeg -y -i music_raw.mp3 -af '
                            f'"volume={MUSIC_VOL},afade=t=in:st=0:d=2,'
                            f'afade=t=out:st=90:d=5" -t 110 {outfile}')
                        self.base.api_status["Music"]["Freesound"] = "success"
                        log_api("music.py", "Freesound", "success")
                        return outfile
                self.base.api_status["Music"]["Freesound"] = "failed"
                log_api("music.py", "Freesound", "failed")
            except Exception as e:
                self.base.api_status["Music"]["Freesound"] = "failed"
                log_api("music.py", "Freesound", "failed", str(e)[:60])

        for idx, u in enumerate([
            "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
            "https://cdn.pixabay.com/download/audio/2022/03/24/audio_4f3b5c5e3d.mp3?filename=peaceful-background-112194.mp3",
        ], 1):
            log_step("music.py", f"Trying Pixabay-CDN #{idx}", "info")
            if self.base.download(u, "music_raw.mp3"):
                self.base.run_cmd(
                    f'ffmpeg -y -i music_raw.mp3 -af '
                    f'"volume={MUSIC_VOL},afade=t=in:st=0:d=2,'
                    f'afade=t=out:st=90:d=5" -t 110 {outfile}')
                self.base.api_status["Music"]["Pixabay-CDN"] = "success"
                log_api("music.py", "Pixabay-CDN", "success")
                return outfile

        log_step("music.py", "Falling back to generated sine", "warn")
        self.base.run_cmd(
            f'ffmpeg -y -f lavfi -i "sine=frequency=110:duration=110" '
            f'-af "afade=t=in:st=0:d=2.5,afade=t=out:st=100:d=6,volume=0.12" {outfile}')
        self.base.api_status["Music"]["Generated-Sine"] = "success (fallback)"
        log_api("music.py", "Generated-Sine", "fallback")
        return outfile
