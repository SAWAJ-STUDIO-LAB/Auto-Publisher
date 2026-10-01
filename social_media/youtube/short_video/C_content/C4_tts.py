# ============================================================
# FILE:      C4_tts.py
# PATH:      social_media/facebook/story_video/C_content/C4_tts.py
# PURPOSE:   Text-to-Speech (ElevenLabs + edge-tts)
# ============================================================

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


class TTS:

    def __init__(self, base):
        log_file_start("C4_tts.py", "Text-to-Speech generation")
        self.base = base
        log_file_end("C4_tts.py", "success", "Ready")

    def generate(self, text, outfile):
        log_step("C4_tts.py", f"generate({outfile})", "ok", f"{len(text)} chars")
        text = sanitize(text)

        el = os.environ.get("ELEVENLABS_API_KEY")
        if el:
            try:
                log_step("C4_tts.py", "Trying ElevenLabs", "info")
                r = self.base.session.post(
                    "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                    headers={
                        "Accept": "audio/mpeg",
                        "Content-Type": "application/json",
                        "xi-api-key": el,
                    },
                    json={
                        "text": text,
                        "model_id": "eleven_multilingual_v2",
                        "voice_settings": {
                            "stability": 0.42,
                            "similarity_boost": 0.82,
                            "style": 0.35,
                            "use_speaker_boost": True,
                        },
                    },
                    timeout=50)
                if r.status_code == 200 and len(r.content) > 5000:
                    with open(outfile, "wb") as f:
                        f.write(r.content)
                    self.base.api_status["TTS"]["ElevenLabs"] = "success"
                    log_api("C4_tts.py", "ElevenLabs", "success",
                            f"{len(r.content)//1024} KB")
                    return True
                self.base.api_status["TTS"]["ElevenLabs"] = "failed"
                log_api("C4_tts.py", "ElevenLabs", "failed", f"HTTP {r.status_code}")
            except Exception as e:
                self.base.api_status["TTS"]["ElevenLabs"] = "failed"
                log_api("C4_tts.py", "ElevenLabs", "failed", str(e)[:60])

        try:
            log_step("C4_tts.py", "Trying edge-tts", "info")
            tmp = outfile + ".txt"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(text)
            self.base.run_cmd(
                f'edge-tts --file "{tmp}" --write-media "{outfile}" '
                f'--voice hi-IN-MadhurNeural --rate=-7% --pitch=-2Hz --volume=+8%')
            if os.path.exists(tmp):
                os.remove(tmp)
            self.base.api_status["TTS"]["edge-tts"] = "success"
            log_api("C4_tts.py", "edge-tts", "success",
                    f"{os.path.getsize(outfile)//1024} KB")
            return True
        except Exception as e:
            self.base.api_status["TTS"]["edge-tts"] = "failed"
            log_api("C4_tts.py", "edge-tts", "failed", str(e)[:60])
            return False
