import os, requests
from .session import get_session

session = get_session()

def deepl_translate(text, target_lang="HI", api_status=None):
    key = os.environ.get("DEEPL_API_KEY")
    if not key:
        if api_status is not None: api_status["Translation"]["DeepL"] = "hold (no key)"
        return None
    try:
        r = session.post("https://api-free.deepl.com/v2/translate",
                         headers={"Authorization": f"DeepL-Auth-Key {key}"},
                         data={"text": text, "target_lang": target_lang}, timeout=30)
        if r.status_code == 200:
            if api_status is not None: api_status["Translation"]["DeepL"] = "success"
            return r.json()["translations"][0]["text"]
    except Exception:
        pass
    if api_status is not None: api_status["Translation"]["DeepL"] = "failed"
    return None
