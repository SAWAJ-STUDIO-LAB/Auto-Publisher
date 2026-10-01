# ============================================================
# 📄 FILE:      F2_upload_short.py
# 📁 PATH:      social_media/facebook/short_video/F_upload/F2_upload_short.py
# 🎯 PURPOSE:   Upload Short video to Facebook Page
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
    # ③ UPLOAD — upload to Facebook Page
    # ─────────────────────────────────────────────────────────
    def upload(self, video_path, caption=""):
        log_step("F2_upload_short.py", f"upload({video_path})", "ok")

        # ───────── Get credentials ─────────
        token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

        if not token or not page_id:
            log_step("F2_upload_short.py", "Missing creds", "fail")
            return False

        try:
            # ───────── Upload video to Page ─────────
            f_size = os.path.getsize(video_path)
            log_step("F2_upload_short.py",
                     f"Uploading {f_size // 1024} KB", "info")

            with open(video_path, "rb") as f:
                res = self.base.session.post(
                    f"https://graph.facebook.com/v21.0/{page_id}/videos",
                    data={
                        "access_token": token,
                        "description": caption,
                        "published": "true",
                    },
                    files={"source": f}, timeout=600).json()

            if res.get("id"):
                self.base.api_status["Facebook"]["Upload"] = "success"
                log_api("F2_upload_short.py", "FB-Short", "success", res["id"])
                return True

            self.base.api_status["Facebook"]["Upload"] = "failed"
            log_api("F2_upload_short.py", "FB-Short", "failed", str(res)[:100])
            return False
        except Exception as e:
            self.base.api_status["Facebook"]["Upload"] = f"failed ({str(e)[:40]})"
            log_api("F2_upload_short.py", "FB-Short", "failed", str(e)[:100])
            return False
