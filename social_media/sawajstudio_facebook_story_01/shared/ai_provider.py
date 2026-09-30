"""
Multi-provider AI caller with automatic fallback.
Providers (in order): OpenRouter → Groq → Gemini → Mistral →
                      Cerebras → Cohere → HuggingFace
"""
import os
from shared.session import session
from shared.telegram import api_status
from shared.logger import get_logger

logger = get_logger("ai")


def _build_providers():
    providers = []
    if os.environ.get("OPENROUTER_API_KEY"):
        providers.append((
            "OpenRouter",
            "https://openrouter.ai/api/v1/chat/completions",
            {"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
            "openai/gpt-4o-mini",
        ))
    if os.environ.get("GROQ_API_KEY"):
        providers.append((
            "Groq",
            "https://api.groq.com/openai/v1/chat/completions",
            {"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
            "llama-3.3-70b-versatile",
        ))
    if os.environ.get("GEMINI_API_KEY"):
        providers.append(("Gemini", None, None, None))
    if os.environ.get("MISTRAL_API_KEY"):
        providers.append((
            "Mistral",
            "https://api.mistral.ai/v1/chat/completions",
            {"Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}"},
            "mistral-small-latest",
        ))
    if os.environ.get("CEREBRAS_API_KEY"):
        providers.append((
            "Cerebras",
            "https://api.cerebras.ai/v1/chat/completions",
            {"Authorization": f"Bearer {os.environ['CEREBRAS_API_KEY']}"},
            "llama3.1-8b",
        ))
    if os.environ.get("COHERE_API_KEY"):
        providers.append((
            "Cohere",
            "https://api.cohere.com/v1/chat",
            {"Authorization": f"Bearer {os.environ['COHERE_API_KEY']}"},
            "command-r-plus",
        ))
    if os.environ.get("HUGGINGFACE_API_KEY"):
        providers.append((
            "HuggingFace",
            "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct",
            {"Authorization": f"Bearer {os.environ['HUGGINGFACE_API_KEY']}"},
            None,
        ))
    return providers


def call_ai(prompt: str, max_tokens: int = 400, task: str = "general"):
    """Try each provider in order. Return text or None."""
    providers = _build_providers()

    for name, url, headers, model in providers:
        try:
            if name == "Gemini":
                r = session.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/"
                    f"gemini-1.5-flash:generateContent?key={os.environ['GEMINI_API_KEY']}",
                    json={"contents": [{"parts": [{"text": prompt}]}]},
                    timeout=40,
                )
                if r.status_code == 200:
                    text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                    api_status["AI"][f"{name}({task})"] = "success"
                    return text

            elif name == "Cohere":
                r = session.post(
                    url,
                    headers={**headers, "Content-Type": "application/json"},
                    json={"model": model, "message": prompt},
                    timeout=40,
                )
                if r.status_code == 200:
                    api_status["AI"][f"{name}({task})"] = "success"
                    return r.json()["text"].strip()

            elif name == "HuggingFace":
                r = session.post(
                    url,
                    headers={**headers, "Content-Type": "application/json"},
                    json={
                        "inputs": prompt,
                        "parameters": {"max_new_tokens": max_tokens, "temperature": 0.7},
                    },
                    timeout=45,
                )
                if r.status_code == 200:
                    data = r.json()
                    if isinstance(data, list) and data:
                        text = data[0].get("generated_text", "").replace(prompt, "").strip()
                        if text:
                            api_status["AI"][f"{name}({task})"] = "success"
                            return text

            else:
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": max_tokens,
                }
                r = session.post(
                    url,
                    headers={**headers, "Content-Type": "application/json"},
                    json=payload,
                    timeout=40,
                )
                if r.status_code == 200:
                    api_status["AI"][f"{name}({task})"] = "success"
                    return r.json()["choices"][0]["message"]["content"].strip()

            api_status["AI"][f"{name}({task})"] = "failed"

        except Exception as e:
            api_status["AI"][f"{name}({task})"] = f"failed ({str(e)[:35]})"

    logger.warning(f"All AI providers failed for task={task}")
    return None
