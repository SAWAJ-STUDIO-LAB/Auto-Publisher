"""
Translation via DeepL (English → Hindi).
"""
import os
from shared.session import session
from shared.telegram import api_status
from shared.logger import get_logger

logger = get_logger("translator")


def deepl(text: str):
    """Translate English text to Hindi. Returns None if no key or failure."""
    key = os.environ.get("DEEPL_API_KEY")
    if not key:
        api_status["Translation"]["DeepL"] = "hold (no key)"
        return None
    try:
        r = session.post(
            "https://api-free.deepl.com/v2/translate",
            headers={"Authorization": f"DeepL-Auth-Key {key}"},
            data={"text": text, "target_lang": "HI"},
            timeout=25,
        )
        if r.status_code == 200:
            api_status["Translation"]["DeepL"] = "success"
            return r.json()["translations"][0]["text"]
        api_status["Translation"]["DeepL"] = "failed"
    except Exception as e:
        api_status["Translation"]["DeepL"] = f"failed ({str(e)[:40]})"
    return None
