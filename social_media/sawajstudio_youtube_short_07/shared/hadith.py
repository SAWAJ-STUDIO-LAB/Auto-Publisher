import os, random, requests
from .session import get_session
from .tts import sanitize

session = get_session()

def fetch_hadith(is_long=False, api_status=None):
    books = [
        {"eng": "eng-bukhari", "ara": "ara-bukhari", "name": "Sahih al-Bukhari", "max": 7000},
        {"eng": "eng-muslim", "ara": "ara-muslim", "name": "Sahih Muslim", "max": 5000},
        {"eng": "eng-abudawud", "ara": "ara-abudawud", "name": "Sunan Abu Dawud", "max": 4000},
        {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi", "name": "Jami at-Tirmidhi", "max": 3500},
    ]
    bases = ["https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1", "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1"]

    for _ in range(20):
        book = random.choice(books)
        num = random.randint(1, book["max"])
        for base in bases:
            try:
                url = f"{base}/editions/{book['eng']}/{num}.json"
                r = session.get(url, timeout=15)
                if r.status_code != 200: continue
                data = r.json()
                hs = data.get("hadiths", [])
                if not hs: continue
                eng = sanitize(hs[0].get("text", ""))

                if is_long and len(eng) < 200: continue
                if not is_long and len(eng) < 30: continue

                if api_status is not None: api_status["Hadith"][f"{book['name']} #{num}"] = "success"
                return {"collection": book["name"], "number": str(hs[0].get("hadithnumber") or num), "english": eng}
            except Exception: pass

    return {
        "collection": "Sahih al-Bukhari", "number": "1",
        "english": "The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended."
    }
