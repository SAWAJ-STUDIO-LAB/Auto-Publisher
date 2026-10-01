# ============================================================
# 📄 FILE:      C1_hadith.py
# 📁 PATH:      social_media/facebook/story_video/C_content/C1_hadith.py
# 🎯 PURPOSE:   Fetch Hadith with LENGTH FILTER for 50-55s video
# ⚠️  NOTE:     Filters by word count — NO TRUNCATION
# ============================================================

import os
import random
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


# ─────────────────────────────────────────────────────────────
# ① HARDCODED FALLBACK (if all APIs fail)
# ─────────────────────────────────────────────────────────────
FALLBACK = {
    "collection": "Sahih al-Bukhari",
    "number": "1",
    "english": "The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.",
    "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
}


# ─────────────────────────────────────────────────────────────
# ② HADITH CLASS
# ─────────────────────────────────────────────────────────────
class Hadith:
    """
    Fetch hadith with word count filter.
    Target: 50-100 words (English) = ~50-55 seconds voice.
    If smaller hadith not found, allow up to 150 words.
    NO TRUNCATION — full hadith always.
    """

    # Word count ranges (English text)
    TARGET_MIN = 50
    TARGET_MAX = 100
    FALLBACK_MIN = 30
    FALLBACK_MAX = 150
    MAX_ATTEMPTS = 25

    # ─────────────────────────────────────────────────────────
    # ③ INIT
    # ─────────────────────────────────────────────────────────
    def __init__(self, base):
        log_file_start("C1_hadith.py", "Fetch Hadith (50-55s filter)")
        self.base = base
        log_file_end("C1_hadith.py", "success", "Ready")

    # ─────────────────────────────────────────────────────────
    # ④ COUNT WORDS
    # ─────────────────────────────────────────────────────────
    def _count_words(self, text):
        """Count words in text."""
        return len(text.split()) if text else 0

    # ─────────────────────────────────────────────────────────
    # ⑤ FETCH ONE — try to fetch one hadith from API
    # ─────────────────────────────────────────────────────────
    def _fetch_one(self, base_url, book, num):
        """Try to fetch one hadith. Returns dict or None."""
        try:
            url = f"{base_url}/editions/{book['eng']}/{num}.json"
            r = self.base.session.get(url, timeout=15)
            if r.status_code != 200:
                return None
            data = r.json()
            hs = data.get("hadiths", [])
            if not hs:
                return None
            eng = sanitize(hs[0].get("text", ""))
            if len(eng) < 30:
                return None

            # Try to get Arabic version
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

            return {
                "collection": book["name"],
                "number": str(hs[0].get("hadithnumber") or num),
                "english": eng,
                "arabic": ara,
                "word_count": self._count_words(eng),
            }
        except Exception:
            return None

    # ─────────────────────────────────────────────────────────
    # ⑥ FETCH — main fetch with 4-phase filtering
    # ─────────────────────────────────────────────────────────
    def fetch(self):
        log_step("C1_hadith.py", "fetch() starting", "ok")

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

        # ═══════════ PHASE 1: Ideal 50-100 words ═══════════
        log_step("C1_hadith.py",
                 f"Phase 1: target {self.TARGET_MIN}-{self.TARGET_MAX} words", "info")
        for attempt in range(self.MAX_ATTEMPTS):
            book = random.choice(books)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h and self.TARGET_MIN <= h["word_count"] <= self.TARGET_MAX:
                    log_api("C1_hadith.py", "Found", "success",
                            f"{h['word_count']} words, #{h['number']}")
                    self.base.api_status["Hadith"]["filtered"] = "success"
                    return {k: v for k, v in h.items() if k != "word_count"}

        # ═══════════ PHASE 2: Fallback 30-150 words ═══════════
        log_step("C1_hadith.py",
                 f"Phase 2: fallback {self.FALLBACK_MIN}-{self.FALLBACK_MAX} words", "warn")
        for attempt in range(self.MAX_ATTEMPTS):
            book = random.choice(books)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h and self.FALLBACK_MIN <= h["word_count"] <= self.FALLBACK_MAX:
                    log_api("C1_hadith.py", "Found (fallback)", "fallback",
                            f"{h['word_count']} words")
                    self.base.api_status["Hadith"]["fallback"] = "success"
                    return {k: v for k, v in h.items() if k != "word_count"}

        # ═══════════ PHASE 3: Any hadith ═══════════
        log_step("C1_hadith.py", "Phase 3: any hadith", "warn")
        for attempt in range(10):
            book = random.choice(books)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h:
                    log_api("C1_hadith.py", "Found (any)", "fallback",
                            f"{h['word_count']} words")
                    return {k: v for k, v in h.items() if k != "word_count"}

        # ═══════════ PHASE 4: Hardcoded fallback ═══════════
        log_api("C1_hadith.py", "Hardcoded-Fallback", "fallback")
        return FALLBACK
