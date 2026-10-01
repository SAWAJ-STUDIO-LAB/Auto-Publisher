# ============================================================
# 📄 FILE:      F2_upload_short.py
# 📁 PATH:      social_media/facebook/short_video/F_upload/F2_upload_short.py
# 🎯 PURPOSE:   Upload Short video to Facebook Page
# ⚠️  NOTE:     Uses System User Token → fetches Page Token → uploads
# ============================================================

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


# ─────────────────────────────────────────────────────────────
# ① SHORT UPLOADER CLASS
# ─────────────────────────────────────────────────────────────
class ShortUploader:
    """Upload video to Facebook Page (as video post)."""

    # ─────────────────────────────────────────────────────────
    # ② INIT
    # ─────────────────────────────────────────────────────────
    def __init__(self, base):
        log_file_start("F2_upload_short.py", "Facebook Short upload")
        self.base = base
        log_file_end("F2_upload_short.py", "success", "Ready")

    # ─────────────────────────────────────────────────────────
    # ③ GET PAGE TOKEN — fetch page access token from system token
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
                log_step("F2_upload_short.py",
                         f"Page token fetch failed: {r['error'].get('message', '')[:60]}",
                         "warn")
                return None

            page_token = r.get("access_token", "")
            page_name = r.get("name", "?")

            if page_token:
                log_step("F2_upload_short.py",
                         f"Page token fetched for {page_name}", "ok")
                return page_token

            log_step("F2_upload_short.py", "No page token in response", "warn")
            return None

        except Exception as e:
            log_step("F2_upload_short.py",
                     f"Page token error: {str(e)[:60]}", "fail")
            return None

    # ─────────────────────────────────────────────────────────
    # ④ UPLOAD — upload to Facebook Page
    # ─────────────────────────────────────────────────────────
    def upload(self, video_path, caption=""):
        log_step("F2_upload_short.py", f"upload({video_path})", "ok")

        # ───────── Get credentials ─────────
        system_token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

        if not system_token:
            log_step("F2_upload_short.py", "META token missing", "fail")
            return False

        if not page_id:
            log_step("F2_upload_short.py", "Page ID missing", "fail")
            return False

        # ───────── Get Page Token (System Token se) ─────────
        log_step("F2_upload_short.py",
                 "Fetching Page Token from System User Token", "info")

        page_token = self._get_page_token(system_token, page_id)

        if not page_token:
            log_step("F2_upload_short.py",
                     "Page token fetch failed — using system token as fallback",
                     "warn")
            page_token = system_token  # Fallback

        # ───────── Upload video with Page Token ─────────
        try:
            f_size = os.path.getsize(video_path)
            log_step("F2_upload_short.py",
                     f"Uploading {f_size // 1024} KB with Page Token", "info")

            with open(video_path, "rb") as f:
                res = self.base.session.post(
                    f"https://graph.facebook.com/v21.0/{page_id}/videos",
                    data={
                        "access_token": page_token,
                        "description": caption,
                        "published": "true",
                    },
                    files={"source": f}, timeout=600).json()

            # ───────── Check response ─────────
            if res.get("id"):
                self.base.api_status["Facebook"]["Upload"] = "success"
                log_api("F2_upload_short.py", "FB-Short", "success", res["id"])
                return True

            # ───────── Log error ─────────
            err = res.get("error", {})
            err_msg = err.get("message", "Unknown error")
            err_code = err.get("code", "?")
            err_subcode = err.get("error_subcode", "")

            log_api("F2_upload_short.py", "FB-Short", "failed",
                    f"Code {err_code}/{err_subcode}: {err_msg[:80]}")

            self.base.api_status["Facebook"]["Upload"] = \
                f"failed (Code {err_code})"
            return False

        except Exception as e:
            self.base.api_status["Facebook"]["Upload"] = f"failed ({str(e)[:40]})"
            log_api("F2_upload_short.py", "FB-Short", "failed", str(e)[:100])
            return False
