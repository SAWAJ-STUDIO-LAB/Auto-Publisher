"""
Hadith fetcher — random from Bukhari/Muslim/AbuDawud/Tirmidhi.
"""
import os
import random
from shared.session import session
from shared.telegram import api_status, send_tg
from shared.utils import sanitize
from shared.logger import get_logger

logger = get_logger("hadith")

BOOKS = [
    {"eng": "eng-bukhari", "ara": "ara-bukhari", "name": "Sahih al-Bukhari", "max": 7000},
    {"eng": "eng-muslim", "ara": "ara-muslim", "name": "Sahih Muslim", "max": 5000},
    {"eng": "eng-abudawud", "ara": "ara-abudawud", "name": "Sunan Abu Dawud", "max": 4000},
    {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi", "name": "Jami at-Tirmidhi", "max": 3500},
]

FALLBACK = {
    "collection": "Sahih al-Bukhari",
    "number": "1",
    "english": (
        "The reward of deeds depends upon the intentions and every person "
        "will get the reward according to what he has intended."
    ),
    "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
}


def _bases():
    bases = []
    custom = os.environ.get("HADITH_API_URL")
    if custom:
        bases.append(custom.rstrip("/"))
    bases += [
        "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
        "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1",
    ]
    return bases


def fetch_hadith() -> dict:
    """Return dict with collection, number, english, arabic."""
    book = random.choice(BOOKS)
    num = random.randint(1, book["max"])

    for base in _bases():
        try:
            url = f"{base}/editions/{book['eng']}/{num}.json"
            r = session.get(url, timeout=15)
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
                ar = session.get(url.replace(book["eng"], book["ara"]), timeout=10)
                if ar.status_code == 200:
                    ad = ar.json().get("hadiths", [])
                    if ad:
                        ara = sanitize(ad[0].get("text", ""))
            except Exception:
                pass

            api_status["Hadith"][base.split("/")[-1] or "custom"] = "success"
            return {
                "collection": book["name"],
                "number": str(hs[0].get("hadithnumber") or num),
                "english": eng,
                "arabic": ara,
            }
        except Exception:
            continue

    api_status["Hadith"]["fallback"] = "success (hardcoded)"
    return FALLBACK
