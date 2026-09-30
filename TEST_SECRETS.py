# ═══════════════════════════════════════════════════════════════════════════
# TOKEN SCOPE + PRIVATE REPO ACCESS TEST
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("🔍 DEEP TOKEN TEST")
print("=" * 60)

# Test 1: Token scopes check
print("\n[Test 1] Checking token scopes...")
gh = os.environ.get("TOKEN_GITHUB", "")
try:
    r = requests.get("https://api.github.com/user",
                     headers={"Authorization": f"token {gh}"}, timeout=15)
    scopes = r.headers.get("x-oauth-scopes", "NONE")
    print(f"   Scopes: {scopes}")

    if "repo" in scopes:
        print("   ✅ 'repo' scope present")
        results.append(("GitHub Scopes", "TOKEN_GITHUB", True, f"✅ {scopes}"))
    else:
        print("   ❌ 'repo' scope MISSING!")
        results.append(("GitHub Scopes", "TOKEN_GITHUB", False, f"❌ No repo scope"))
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Private repo access
print("\n[Test 2] Testing private repo access...")
try:
    r = requests.get("https://api.github.com/repos/SAWAJ-STUDIO-LAB/admin",
                     headers={"Authorization": f"token {gh}"}, timeout=15)
    print(f"   HTTP Status: {r.status_code}")

    if r.status_code == 200:
        print("   ✅ Private repo ACCESSIBLE")
        results.append(("Private Repo Access", "TOKEN_GITHUB", True, "✅ Accessible"))
    elif r.status_code == 404:
        print("   ❌ Private repo NOT accessible (404 = no access)")
        results.append(("Private Repo Access", "TOKEN_GITHUB", False, "❌ 404 - No access"))
    elif r.status_code == 401:
        print("   ❌ Token INVALID (401)")
        results.append(("Private Repo Access", "TOKEN_GITHUB", False, "❌ 401 - Invalid"))
    else:
        print(f"   ⚠️ Status {r.status_code}: {r.text[:150]}")
        results.append(("Private Repo Access", "TOKEN_GITHUB", False, f"⚠️ Status {r.status_code}"))
except Exception as e:
    print(f"   ❌ Error: {e}")
    results.append(("Private Repo Access", "TOKEN_GITHUB", False, f"❌ {str(e)[:50]}"))
