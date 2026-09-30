"""Fetch random Hadith."""
import os
import random
from utils import sanitize
from logger import log_file_start, log_file_end, log_step, log_api


FALLBACK = {
    "collection": "Sahih al-Bukhari",
    "number": "1",
    "english": "The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.",
    "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
}


class Hadith:
    def __init__(self, base):
        log_file_start("hadith.py", "Fetch random Hadith (EN + AR)")
        self.base = base
        log_file_end("hadith.py", "success", "Ready")

    def fetch(self):
        log_step("hadith.py", "fetch() starting", "ok")

        books = [
            {"eng": "eng-bukhari", "ara": "ara-bukhari",
             "name": "Sahih al-Bukhari", "max": 7000},
            {"eng": "eng-muslim", "ara": "ara-muslim",
             "name": "Sahih Muslim", "max": 5000},
            {"eng": "eng-abudawud", "ara": "ara-abudawud",
             "name": "Sunan Abu Dawud", "max": 4000},
            {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi",
             "name": "Jami at-Tirmidhi", "max": 3500},
        ]

        bases = []
        if os.environ.get("HADITH_API_URL"):
            bases.append(os.environ["HADITH_API_URL"].rstrip("/"))
        bases += [
            "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
            "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1",
        ]

        book = random.choice(books)
        num = random.randint(1, book["max"])
        log_step("hadith.py", f"Chose {book['name']} #{num}", "ok")

        for base in bases:
            try:
                url = f"{base}/editions/{book['eng']}/{num}.json"
                log_step("hadith.py", f"Trying {base[:40]}...", "info")
                r = self.base.session.get(url, timeout=15)
                if r.status_code != 200:
                    continue
                data = r.json()
                hs = data.get("hadiths", [])
                if not hs:
                    continue
                eng = sanitize(hs[0].get("text", ""))
                if len(eng) < 30:
                    continue

                ara = ""
                try:
                    ar = self.base.session.get(
                        url.replace(book["eng"], book["ara"]), timeout=10)
                    if ar.status_code == 200:
                        ad = ar.json().get("hadiths", [])
                        if ad:
                            ara = sanitize(ad[0].get("text", ""))
                except Exception:
                    pass

                self.base.api_status["Hadith"][
                    base.split("/")[-1] or "custom"] = "success"
                log_api("hadith.py", base.split("/")[-1][:30], "success",
                        f"EN={len(eng)} AR={len(ara)} chars")

                return {
                    "collection": book["name"],
                    "number": str(hs[0].get("hadithnumber") or num),
                    "english": eng,
                    "arabic": ara,
                }
            except Exception as e:
                log_step("hadith.py", f"Err base {base[:40]}", "fail", str(e)[:60])

        self.base.api_status["Hadith"]["fallback"] = "success (hardcoded)"
        log_api("hadith.py", "Hardcoded-Fallback", "fallback")
        return FALLBACK
