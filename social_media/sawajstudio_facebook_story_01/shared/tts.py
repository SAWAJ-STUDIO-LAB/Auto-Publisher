"""
Text-to-Speech: ElevenLabs → edge-tts fallback.
"""
import os
from shared.session import session
from shared.telegram import api_status
from shared.utils import sanitize, run_cmd
from shared.logger import get_logger

logger = get_logger("tts")

# Hindi male voice, matches original workflow
ELEVENLABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"
EDGE_VOICE = "hi-IN-MadhurNeural"


def gen_tts(text: str, outfile: str) -> bool:
    """Generate TTS. Returns True on success."""
    text = sanitize(text)

    # Try ElevenLabs first
    el = os.environ.get("ELEVENLABS_API_KEY")
    if el:
        try:
            r = session.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
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
                timeout=50,
            )
            if r.status_code == 200 and len(r.content) > 5000:
                with open(outfile, "wb") as f:
                    f.write(r.content)
                api_status["TTS"]["ElevenLabs"] = "success"
                return True
            api_status["TTS"]["ElevenLabs"] = "failed"
        except Exception as e:
            api_status["TTS"]["ElevenLabs"] = f"failed ({str(e)[:35]})"

    # Fallback to edge-tts
    try:
        tmp = outfile + ".txt"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        run_cmd(
            f'edge-tts --file "{tmp}" --write-media "{outfile}" '
            f'--voice {EDGE_VOICE} --rate=-7% --pitch=-2Hz --volume=+8%'
        )
        if os.path.exists(tmp):
            os.remove(tmp)
        api_status["TTS"]["edge-tts"] = "success"
        return True
    except Exception as e:
        api_status["TTS"]["edge-tts"] = f"failed ({str(e)[:35]})"
        return False
