import os
import sys
import requests


def get_env_variable(keys, default=None):
    """Multiple env variables me se sabse pehla active variable retrieve karta hai."""
    for key in keys:
        val = os.environ.get(key)
        if val and val.strip():
            return val.strip()
    return default


def cleanup_old_caches():
    # Auto-detect Token, Repo, aur Cache Version
    token = get_env_variable(["GH_TOKEN", "TOKEN_GITHUB", "GITHUB_TOKEN"])
    repo = get_env_variable(["REPO", "GITHUB_REPOSITORY"])
    cache_version = get_env_variable(["CACHE_VERSION"], "v12")

    if not token:
        print("❌ Error: GitHub Token nahi mila! GH_TOKEN, TOKEN_GITHUB, ya GITHUB_TOKEN set karein.")
        sys.exit(1)

    if not repo:
        print("❌ Error: Repository name nahi mila! REPO ya GITHUB_REPOSITORY env variable missing hai.")
        sys.exit(1)

    print(f"🔍 Starting Cache Cleanup for Repo: [{repo}]")
    print(f"📌 Keeping Cache Version: [{cache_version}]\n")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    page = 1
    per_page = 100
    deleted_count = 0
    kept_count = 0

    while True:
        url = f"https://api.github.com/repos/{repo}/actions/caches?per_page={per_page}&page={page}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 403:
                print("❌ Permission Error (403): Ensure your token has 'actions: write' permissions.")
                break
            elif response.status_code == 404:
                print(f"❌ Not Found (404): Repo '{repo}' nahi mili ya token ke paas access nahi hai.")
                break
            elif response.status_code != 200:
                print(f"⚠ Cache fetch error: HTTP {response.status_code} - {response.text}")
                break

            data = response.json()
            caches = data.get("actions_caches", [])

            if not caches:
                if page == 1:
                    print("✅ Koi cache nahi mila.")
                break

            for cache in caches:
                key = cache.get("key", "")
                cache_id = cache.get("id")
                size_in_bytes = cache.get("size_in_bytes", 0)
                size_mb = round(size_in_bytes / (1024 * 1024), 2)

                # Version check logic: agar version match nahi hota toh delete kar do
                if cache_version not in key:
                    del_url = f"https://api.github.com/repos/{repo}/actions/caches/{cache_id}"
                    del_res = requests.delete(del_url, headers=headers, timeout=15)
                    
                    if del_res.status_code in [200, 204]:
                        print(f"🗑️️ Deleted: {key} ({size_mb} MB)")
                        deleted_count += 1
                    else:
                        print(f"❌ Delete failed for {key}: HTTP {del_res.status_code}")
                else:
                    print(f"✅ Kept (Safe): {key} ({size_mb} MB)")
                    kept_count += 1

            total_count = data.get("total_count", 0)
            if page * per_page >= total_count or len(caches) < per_page:
                break
            
            page += 1

        except Exception as e:
            print(f"⚠ Exception in cleanup: {e}")
            break

    print("\n" + "=" * 40)
    print("📊 CLEANUP SUMMARY")
    print(f"   - Deleted Caches: {deleted_count}")
    print(f"   - Kept Caches:    {kept_count}")
    print("=" * 40)


if __name__ == "__main__":
    cleanup_old_caches()
