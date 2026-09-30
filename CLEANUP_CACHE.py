# ═══════════════════════════════════════════════════════════════════════════
# CLEANUP_CACHE.PY — Auto Cache Cleanup
# ═══════════════════════════════════════════════════════════════════════════
# KAAM: GitHub Actions ke purane cache delete karo
#
# RULES:
#   1. 7+ din purane saare cache delete
#   2. Purane version wale cache delete
#   3. Current version wale cache rakh do
#
# ENV VARS:
#   GH_TOKEN        - GitHub token (secrets.TOKEN_GITHUB)
#   REPO            - Repository name (github.repository)
#   CACHE_VERSION   - Current cache version (v12)
# ═══════════════════════════════════════════════════════════════════════════

# [01] Imports
import os
import sys
import json
import requests
from datetime import datetime, timezone

# [02] Environment variables
GH_TOKEN = os.environ.get("GH_TOKEN", "")
REPO = os.environ.get("REPO", "")
CURRENT_VERSION = os.environ.get("CACHE_VERSION", "v12")

# [03] Validation
if not GH_TOKEN:
    print("❌ GH_TOKEN missing — cleanup skip")
    sys.exit(0)

if not REPO:
    print("❌ REPO missing — cleanup skip")
    sys.exit(0)

print(f"🧹 Auto Cache Cleanup shuru...")
print(f"📦 Repo: {REPO}")
print(f"📦 Current cache version: {CURRENT_VERSION}")
print("")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: Saare caches list karo (GitHub API se)
# ═══════════════════════════════════════════════════════════════════════════
print("🔍 Fetching caches from GitHub API...")

try:
    r = requests.get(
        f"https://api.github.com/repos/{REPO}/actions/caches?per_page=100",
        headers={
            "Authorization": f"token {GH_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        timeout=30,
    )

    if r.status_code != 200:
        print(f"❌ API error: {r.status_code}")
        print(r.text[:500])
        sys.exit(0)

    data = r.json()
    caches = data.get("actions_caches", [])
    total = len(caches)

    print(f"📊 Total caches found: {total}")
    print("")

    if total == 0:
        print("✅ Koi cache nahi hai — cleanup skip")
        sys.exit(0)

except Exception as e:
    print(f"❌ Exception: {e}")
    sys.exit(0)


# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: Har cache check karo + delete karo
# ═══════════════════════════════════════════════════════════════════════════
now = datetime.now(timezone.utc)
deleted = 0
kept = 0

for cache in caches:
    cache_id = cache.get("id")
    cache_key = cache.get("key", "")
    cache_size = cache.get("size_in_bytes", 0) / (1024 * 1024)  # MB

    # [04] Age calculate karo
    created_str = cache.get("created_at", "")
    try:
        created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
        days_old = (now - created).days
    except Exception:
        days_old = 999

    # [05] Delete rules
    should_delete = False
    reason = ""

    # Rule 1: 7+ din purana
    if days_old >= 7:
        should_delete = True
        reason = f"{days_old} days old"

    # Rule 2: Purana version
    elif f"-{CURRENT_VERSION}-" not in cache_key:
        should_delete = True
        reason = "old version"

    # [06] Delete karo
    if should_delete:
        print(f"🗑️  Deleting: {cache_key[:70]}")
        print(f"   Size: {cache_size:.1f} MB | Age: {days_old} days | Reason: {reason}")

        try:
            del_r = requests.delete(
                f"https://api.github.com/repos/{REPO}/actions/caches/{cache_id}",
                headers={
                    "Authorization": f"token {GH_TOKEN}",
                    "Accept": "application/vnd.github+json",
                },
                timeout=30,
            )

            if del_r.status_code in [200, 204]:
                deleted += 1
                print(f"   ✅ Deleted")
            else:
                print(f"   ⚠️ Delete failed: {del_r.status_code}")
        except Exception as e:
            print(f"   ⚠️ Exception: {e}")
    else:
        print(f"✅ Keeping: {cache_key[:70]}")
        print(f"   Size: {cache_size:.1f} MB | Age: {days_old} days")
        kept += 1

    print("")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: Summary
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 60)
print(f"📊 Summary: Deleted {deleted} | Kept {kept}")
print("=" * 60)
print("✅ Auto cache cleanup complete!")
