# ============================================================
# 📄 FILE:      F2_upload_long.py
# 📁 PATH:      social_media/facebook/long_video/F_upload/F2_upload_long.py
# 🎯 PURPOSE:   Upload Long video to Facebook Page (with chapters)
# ⚠️  NOTE:     Uses System User Token → Page Token → uploads
# ============================================================

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class LongUploader:
    """Upload long video to Facebook Page (as video post)."""

    def __init__(self, base):
        log_file_start("F2_upload_long.py", "Facebook Long upload")
        self.base = base
        log_file_end("F2_upload_long.py", "success", "Ready")

    # ─────────────────────────────────────────────────────────
    # ① GET PAGE TOKEN
    # ─────────────────────────────────────────────────────────
    def _get_page_token(self, system_token, page_id):
        """Fetch Page Access Token using System User Token."""
        try:
            r = self.base.session.get(
                f"https://graph.facebook.com/v21.0/{page_id}",
                params={
                    "fields": "access_token,name",
                    "access_token": system_token,
                },
                timeout=15).json()

            if r.get("error"):
                log_step("F2_upload_long.py",
                         f"Page token fetch failed: {r['error'].get('message', '')[:60]}",
                         "warn")
                return None

            page_token = r.get("access_token", "")
            page_name = r.get("name", "?")

            if page_token:
                log_step("F2_upload_long.py",
                         f"Page token fetched for {page_name}", "ok")
                return page_token

            return None
        except Exception as e:
            log_step("F2_upload_long.py",
                     f"Page token error: {str(e)[:60]}", "fail")
            return None

    # ─────────────────────────────────────────────────────────
    # ② UPLOAD
    # ─────────────────────────────────────────────────────────
    def upload(self, video_path, caption=""):
        log_step("F2_upload_long.py", f"upload({video_path})", "ok")

        system_token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

        if not system_token or not page_id:
            log_step("F2_upload_long.py", "Missing creds", "fail")
            return False

        # ───────── Get Page Token ─────────
        log_step("F2_upload_long.py",
                 "Fetching Page Token from System User Token", "info")

        page_token = self._get_page_token(system_token, page_id) or system_token

        try:
            f_size = os.path.getsize(video_path)
            log_step("F2_upload_long.py",
                     f"Uploading {f_size // 1024} KB with Page Token", "info")

            with open(video_path, "rb") as f:
                res = self.base.session.post(
                    f"https://graph.facebook.com/v21.0/{page_id}/videos",
                    data={
                        "access_token": page_token,
                        "description": caption,
                        "published": "true",
                    },
                    files={"source": f}, timeout=1800).json()

            if res.get("id"):
                self.base.api_status["Facebook"]["Upload"] = "success"
                log_api("F2_upload_long.py", "FB-Long", "success", res["id"])
                return True

            if res.get("error"):
                err = res["error"]
                log_api("F2_upload_long.py", "FB-Long", "failed",
                        f"Code {err.get('code', '?')}: {err.get('message', '')[:80]}")
                return False

            log_api("F2_upload_long.py", "FB-Long", "failed", "unknown")
            return False
        except Exception as e:
            self.base.api_status["Facebook"]["Upload"] = f"failed ({str(e)[:40]})"
            log_api("F2_upload_long.py", "FB-Long", "failed", str(e)[:100])
            return False
