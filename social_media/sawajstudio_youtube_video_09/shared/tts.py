import os, re, subprocess, requests
from .session import get_session

session = get_session()

def sanitize(t):
    if not t: return ""
    t = re.sub(r"[\u200b-\u200f\ufeff\u202a-\u202e]", "", str(t))
    return t.replace("\"", "").replace("\x27", "").replace("\n", " ").strip()

def gen_tts(text, outfile, rate="-9%", api_status=None):
    text = sanitize(text)
    el = os.environ.get("ELEVENLABS_API_KEY")
    if el:
        try:
            r = session.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                             headers={"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": el},
                             json={"text": text, "model_id": "eleven_multilingual_v2",
                                   "voice_settings": {"stability": 0.42, "similarity_boost": 0.82, "style": 0.35, "use_speaker_boost": True}},
                             timeout=70)
            if r.status_code == 200 and len(r.content) > 5000:
                open(outfile, "wb").write(r.content)
                if api_status is not None: api_status["TTS"]["ElevenLabs"] = "success"
                return True
        except Exception:
            pass

    try:
        tmp = outfile + ".txt"
        open(tmp, "w", encoding="utf-8").write(text)
        subprocess.run(f"edge-tts --file \"{tmp}\" --write-media \"{outfile}\" --voice hi-IN-MadhurNeural --rate={rate} --pitch=-2Hz --volume=+8%", shell=True, check=True)
        if os.path.exists(tmp): os.remove(tmp)
        if api_status is not None: api_status["TTS"]["edge-tts"] = "success"
        return True
    except Exception:
        if api_status is not None: api_status["TTS"]["edge-tts"] = "failed"
        return False
