"""Translator — DeepL + AI fallback."""
import os
from logger import log_file_start, log_file_end, log_step, log_api


class Translator:
    def __init__(self, base, ai):
        log_file_start("translator.py", "English → Hindi translation")
        self.base = base
        self.ai = ai
        log_file_end("translator.py", "success", "Ready")

    def deepl(self, text):
        key = os.environ.get("DEEPL_API_KEY")
        if not key:
            self.base.api_status["Translation"]["DeepL"] = "hold (no key)"
            log_api("translator.py", "DeepL", "skipped", "no key")
            return None
        try:
            r = self.base.session.post(
                "https://api-free.deepl.com/v2/translate",
                headers={"Authorization": f"DeepL-Auth-Key {key}"},
                data={"text": text, "target_lang": "HI"},
                timeout=25)
            if r.status_code == 200:
                self.base.api_status["Translation"]["DeepL"] = "success"
                out = r.json()["translations"][0]["text"]
                log_api("translator.py", "DeepL", "success", f"{len(out)} chars")
                return out
            self.base.api_status["Translation"]["DeepL"] = "failed"
            log_api("translator.py", "DeepL", "failed", f"HTTP {r.status_code}")
        except Exception as e:
            self.base.api_status["Translation"]["DeepL"] = "failed"
            log_api("translator.py", "DeepL", "failed", str(e)[:60])
        return None

    def to_hindi(self, english):
        log_step("translator.py", "to_hindi()", "ok")
        hindi = self.deepl(english)
        if hindi:
            return hindi
        log_step("translator.py", "DeepL failed → AI fallback", "warn")
        result = self.ai.call(
            f"Is English Hadith ka soft accurate Hindi tarjuma likho. "
            f"Sirf tarjuma. Koi extra baat mat likho.\n\n{english}",
            task="hindi")
        if result:
            log_step("translator.py", "AI translation done", "ok")
            return result
        log_step("translator.py", "Using hardcoded fallback", "warn")
        return "अमल का दारोमदार नीयतों पर है।"
