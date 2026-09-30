import os, requests
from .session import get_session

session = get_session()

def call_ai(prompt, max_tokens=500, task="general", api_status=None):
    providers = []
    if os.environ.get("OPENROUTER_API_KEY"):
        providers.append(("OpenRouter", "https://openrouter.ai/api/v1/chat/completions",
                          {"Authorization": f"Bearer {os.environ[OPENROUTER_API_KEY]}"}, "openai/gpt-4o-mini"))
    if os.environ.get("GROQ_API_KEY"):
        providers.append(("Groq", "https://api.groq.com/openai/v1/chat/completions",
                          {"Authorization": f"Bearer {os.environ[GROQ_API_KEY]}"}, "llama-3.3-70b-versatile"))
    if os.environ.get("GEMINI_API_KEY"):
        providers.append(("Gemini", None, None, None))

    for name, url, headers, model in providers:
        try:
            if name == "Gemini":
                r = session.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={os.environ[GEMINI_API_KEY]}",
                    json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45
                )
                if r.status_code == 200:
                    if api_status is not None: api_status["AI"][f"{name}({task})"] = "success"
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": max_tokens}
                r = session.post(url, headers={**headers, "Content-Type": "application/json"}, json=payload, timeout=45)
                if r.status_code == 200:
                    if api_status is not None: api_status["AI"][f"{name}({task})"] = "success"
                    return r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if api_status is not None: api_status["AI"][f"{name}({task})"] = f"failed ({str(e)[:35]})"
    return None
