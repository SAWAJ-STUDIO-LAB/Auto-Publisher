# ═══════════════════════════════════════════════════════════════════════════
# TEST_SECRETS.PY — Saare secrets test karo
# ═══════════════════════════════════════════════════════════════════════════
# KAAM: Har API key ko ping karo, status report Telegram par bhejo.
# ═══════════════════════════════════════════════════════════════════════════

# [01] Imports
import os
import sys
import time
import json
import requests

# [02] Telegram credentials
TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TG_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "")

# [03] Results store karo
results = []
start_time = time.time()


# [04] test() — Ek API ko test karo
def test(name, url, headers=None, method="GET", data=None):
    """
    KAAM: Kisi bhi API endpoint ko ping karo.
    Return: (success_bool, status_code, message)
    """
    try:
        if method == "GET":
            r = requests.get(url, headers=headers or {}, timeout=15)
        else:
            r = requests.post(url, headers=headers or {}, data=data or {}, timeout=15)

        if r.status_code in [200, 201]:
            return True, r.status_code, "✅ Working"
        elif r.status_code in [401, 403]:
            return False, r.status_code, "❌ Auth failed"
        elif r.status_code == 404:
            return False, r.status_code, "❌ Not found"
        else:
            return False, r.status_code, f"⚠️ Status {r.status_code}"
    except Exception as e:
        return False, 0, f"❌ {str(e)[:50]}"


# [05] Header print karo
print("=" * 60)
print("🧪 SECRET TESTING STARTED")
print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 1: Telegram
# ═══════════════════════════════════════════════════════════════════════════
print("\n[1/17] Testing Telegram...")
ok, code, msg = test("telegram", f"https://api.telegram.org/bot{TG_TOKEN}/getMe")
results.append(("Telegram Bot", "TELEGRAM_BOT_TOKEN", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 2: GitHub Token
# ═══════════════════════════════════════════════════════════════════════════
print("\n[2/17] Testing GitHub...")
gh = os.environ.get("TOKEN_GITHUB", "")
ok, code, msg = test("github", "https://api.github.com/user",
                     headers={"Authorization": f"token {gh}"})
results.append(("GitHub API", "TOKEN_GITHUB", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 3: OpenRouter
# ═══════════════════════════════════════════════════════════════════════════
print("\n[3/17] Testing OpenRouter...")
or_key = os.environ.get("OPENROUTER_API_KEY_AI", "")
ok, code, msg = test("openrouter", "https://openrouter.ai/api/v1/models",
                     headers={"Authorization": f"Bearer {or_key}"})
results.append(("OpenRouter", "OPENROUTER_API_KEY_AI", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 4: Groq
# ═══════════════════════════════════════════════════════════════════════════
print("\n[4/17] Testing Groq...")
gr_key = os.environ.get("GROQ_API_KEY_AI", "")
ok, code, msg = test("groq", "https://api.groq.com/openai/v1/models",
                     headers={"Authorization": f"Bearer {gr_key}"})
results.append(("Groq", "GROQ_API_KEY_AI", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 5: Gemini
# ═══════════════════════════════════════════════════════════════════════════
print("\n[5/17] Testing Gemini...")
gm_key = os.environ.get("GEMINI_API_KEY_AI", "")
ok, code, msg = test("gemini",
                     f"https://generativelanguage.googleapis.com/v1beta/models?key={gm_key}")
results.append(("Gemini", "GEMINI_API_KEY_AI", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 6: Mistral
# ═══════════════════════════════════════════════════════════════════════════
print("\n[6/17] Testing Mistral...")
mi_key = os.environ.get("MISTRAL_API_KEY_AI", "")
ok, code, msg = test("mistral", "https://api.mistral.ai/v1/models",
                     headers={"Authorization": f"Bearer {mi_key}"})
results.append(("Mistral", "MISTRAL_API_KEY_AI", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 7: Cerebras
# ═══════════════════════════════════════════════════════════════════════════
print("\n[7/17] Testing Cerebras...")
ce_key = os.environ.get("CEREBRAS_API_KEY_AI", "")
ok, code, msg = test("cerebras", "https://api.cerebras.ai/v1/models",
                     headers={"Authorization": f"Bearer {ce_key}"})
results.append(("Cerebras", "CEREBRAS_API_KEY_AI", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 8: Cohere
# ═══════════════════════════════════════════════════════════════════════════
print("\n[8/17] Testing Cohere...")
co_key = os.environ.get("COHERE_API_KEY_AI", "")
ok, code, msg = test("cohere", "https://api.cohere.ai/v1/models",
                     headers={"Authorization": f"Bearer {co_key}"})
results.append(("Cohere", "COHERE_API_KEY_AI", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 9: HuggingFace
# ═══════════════════════════════════════════════════════════════════════════
print("\n[9/17] Testing HuggingFace...")
hf_key = os.environ.get("HUGGINGFACE_API_KEY_AI", "")
ok, code, msg = test("huggingface", "https://huggingface.co/api/whoami-v2",
                     headers={"Authorization": f"Bearer {hf_key}"})
results.append(("HuggingFace", "HUGGINGFACE_API_KEY_AI", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 10: Jina AI
# ═══════════════════════════════════════════════════════════════════════════
print("\n[10/17] Testing Jina AI...")
jn_key = os.environ.get("JINA_API_KEY", "")
ok, code, msg = test("jina", "https://api.jina.ai/v1/embeddings",
                     headers={"Authorization": f"Bearer {jn_key}"},
                     method="POST",
                     data={"input": ["test"], "model": "jina-embeddings-v2-base-en"})
results.append(("Jina AI", "JINA_API_KEY", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 11: Pexels
# ═══════════════════════════════════════════════════════════════════════════
print("\n[11/17] Testing Pexels...")
px_key = os.environ.get("PEXELS_API_KEY", "")
ok, code, msg = test("pexels",
                     "https://api.pexels.com/v1/search?query=test&per_page=1",
                     headers={"Authorization": px_key})
results.append(("Pexels", "PEXELS_API_KEY", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 12: Pixabay
# ═══════════════════════════════════════════════════════════════════════════
print("\n[12/17] Testing Pixabay...")
pb_key = os.environ.get("PIXABAY_API_KEY", "")
ok, code, msg = test("pixabay",
                     f"https://pixabay.com/api/?key={pb_key}&q=test&per_page=3")
results.append(("Pixabay", "PIXABAY_API_KEY", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 13: Freesound
# ═══════════════════════════════════════════════════════════════════════════
print("\n[13/17] Testing Freesound...")
fs_key = os.environ.get("FREESOUND_API_KEY", "")
ok, code, msg = test("freesound",
                     f"https://freesound.org/apiv2/search/text/?query=rain&token={fs_key}")
results.append(("Freesound", "FREESOUND_API_KEY", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 14: ElevenLabs
# ═══════════════════════════════════════════════════════════════════════════
print("\n[14/17] Testing ElevenLabs...")
el_key = os.environ.get("ELEVENLABS_API_KEY", "")
ok, code, msg = test("elevenlabs", "https://api.elevenlabs.io/v1/user",
                     headers={"xi-api-key": el_key})
results.append(("ElevenLabs", "ELEVENLABS_API_KEY", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 15: DeepL
# ═══════════════════════════════════════════════════════════════════════════
print("\n[15/17] Testing DeepL...")
dl_key = os.environ.get("DEEPL_API_KEY", "")
ok, code, msg = test("deepl", "https://api-free.deepl.com/v2/usage",
                     headers={"Authorization": f"DeepL-Auth-Key {dl_key}"})
results.append(("DeepL", "DEEPL_API_KEY", ok, msg))
print(f"   {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 16: Facebook Page ID (Presence check)
# ═══════════════════════════════════════════════════════════════════════════
print("\n[16/17] Testing Facebook Page ID...")
fb_page = os.environ.get("FACEBOOK_PAGE_ID", "")
if fb_page:
    results.append(("Facebook Page ID", "FACEBOOK_PAGE_ID", True, "✅ Present"))
    print("   ✅ Present")
else:
    results.append(("Facebook Page ID", "FACEBOOK_PAGE_ID", False, "❌ Missing"))
    print("   ❌ Missing")


# ═══════════════════════════════════════════════════════════════════════════
# TEST 17: Google Drive Folder ID (Presence check)
# ═══════════════════════════════════════════════════════════════════════════
print("\n[17/17] Testing Google Drive Folder ID...")
gd_folder = os.environ.get("GDRIVE_STORY_VIDEO_FOLDER_ID", "")
if gd_folder:
    results.append(("GDrive Story Folder", "GDRIVE_STORY_VIDEO_FOLDER_ID", True, "✅ Present"))
    print("   ✅ Present")
else:
    results.append(("GDrive Story Folder", "GDRIVE_STORY_VIDEO_FOLDER_ID", False, "❌ Missing"))
    print("   ❌ Missing")


# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY BUILD
# ═══════════════════════════════════════════════════════════════════════════
total = len(results)
passed = sum(1 for r in results if r[2])
failed = total - passed
elapsed = time.time() - start_time

# [06] Telegram report text banao
lines = [
    "⚡ <b>SAWAJSTUDIO SECRET TEST</b> ⚡",
    "━━━━━━━━━━━━━━━━━━━━━━",
    f"📊 <b>Total:</b> {total}",
    f"🟢 <b>Working:</b> {passed}",
    f"🔴 <b>Failed:</b> {failed}",
    f"⏱ <b>Speed:</b> {elapsed:.2f}s",
    "━━━━━━━━━━━━━━━━━━━━━━",
    "",
]

for name, key, ok, msg in results:
    icon = "🟢" if ok else "🔴"
    lines.append(f"{icon} <b>{name}</b>")
    lines.append(f"   <code>{key}</code> — {msg}")
    lines.append("")

lines.append("━━━━━━━━━━━━━━━━━━━━━━")
if failed == 0:
    lines.append("✅ <b>ALL SYSTEMS OPERATIONAL</b> 🚀")
else:
    lines.append(f"⚠️ <b>{failed} SECRET(S) NEED ATTENTION</b>")

report = "\n".join(lines)

# [07] Console par print karo
print("\n" + "=" * 60)
print(report)
print("=" * 60)

# [08] Telegram par bhejo
if TG_TOKEN and TG_CHAT:
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        r = requests.post(url, data={
            "chat_id": TG_CHAT,
            "text": report,
            "parse_mode": "HTML",
        }, timeout=30)
        print(f"\n📱 Telegram report sent: {r.status_code}")
    except Exception as e:
        print(f"\n❌ Telegram error: {e}")
else:
    print("\n⚠️ Telegram credentials missing")

# [09] Exit code
sys.exit(0 if failed == 0 else 1)
