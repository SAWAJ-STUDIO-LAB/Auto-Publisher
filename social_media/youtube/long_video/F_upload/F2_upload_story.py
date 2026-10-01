# ============================================================
# FILE:      F2_upload_story.py
# PATH:      social_media/facebook/story_video/F_upload/F2_upload_story.py
# PURPOSE:   Facebook Story upload via Graph API
# ============================================================

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class StoryUploader:

    def __init__(self, base):
        log_file_start("F2_upload_story.py", "Facebook Story upload")
        self.base = base
        log_file_end("F2_upload_story.py", "success", "Ready")

    def upload(self, video_path):
        log_step("F2_upload_story.py", f"upload({video_path})", "ok")

        token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
        if not token:
            log_step("F2_upload_story.py", "META token missing", "fail")
            return False

        page_token = token
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

        try:
            acc = self.base.session.get(
                "https://graph.facebook.com/v21.0/me/accounts",
                params={"access_token": page_token, "limit": 40},
                timeout=15).json()
            if acc.get("data"):
                for p in acc["data"]:
                    if not page_id or p["id"] == page_id:
                        page_id = p["id"]
                        if p.get("access_token"):
                            page_token = p["access_token"]
                        log_step("F2_upload_story.py",
                                 f"Page resolved: {page_id}", "ok")
                        break
        except Exception as e:
            log_step("F2_upload_story.py", "Page resolve failed", "warn",
                     str(e)[:60])

        if not page_id:
            log_step("F2_upload_story.py", "Page ID missing", "fail")
            return False

        try:
            f_size = os.path.getsize(video_path)
            log_step("F2_upload_story.py",
                     f"Starting upload ({f_size // 1024} KB)", "info")

            start = self.base.session.post(
                f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
                data={"upload_phase": "start",
                      "file_size": f_size,
                      "access_token": page_token},
                timeout=30).json()
            v_id = start.get("video_id")
            v_url = start.get("upload_url")

            if v_id and v_url:
                with open(video_path, "rb") as f:
                    up_res = self.base.session.post(
                        v_url,
                        headers={
                            "Authorization": f"OAuth {page_token}",
                            "offset": "0",
                            "file_size": str(f_size),
                        },
                        data=f.read(), timeout=180)

                if up_res.status_code in (200, 201):
                    finish = self.base.session.post(
                        f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
                        data={"upload_phase": "finish",
                              "video_id": v_id,
                              "access_token": page_token},
                        timeout=30).json()
                    if finish.get("success") or finish.get("post_id"):
                        self.base.api_status["Facebook Story"]["Upload"] = "success"
                        log_api("F2_upload_story.py", "FB-Story", "success")
                        return True

            self.base.api_status["Facebook Story"]["Upload"] = "failed"
            log_api("F2_upload_story.py", "FB-Story", "failed")
            return False
        except Exception as e:
            self.base.api_status["Facebook Story"]["Upload"] = f"failed ({str(e)[:40]})"
            log_api("F2_upload_story.py", "FB-Story", "failed", str(e)[:100])
            return False
