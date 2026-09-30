"""Facebook Story upload via Graph API."""
import os
from telegram import send_tg
from logger import log_file_start, log_file_end, log_step, log_api


class StoryUploader:
    def __init__(self, base):
        log_file_start("upload_story.py", "Facebook Story upload")
        self.base = base
        log_file_end("upload_story.py", "success", "Ready")

    def upload(self, video_path):
        log_step("upload_story.py", f"upload({video_path})", "ok")
        token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
        if not token:
            log_step("upload_story.py", "META token missing", "fail")
            send_tg("❌ Facebook: META token missing")
            return False

        page_token = token
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

        try:
            log_step("upload_story.py", "Resolving page token", "info")
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
                        log_step("upload_story.py", f"Page resolved: {page_id}", "ok")
                        break
        except Exception as e:
            log_step("upload_story.py", "Page resolve failed", "warn", str(e)[:60])

        if not page_id:
            log_step("upload_story.py", "Page ID missing", "fail")
            send_tg("❌ Facebook: Page ID missing")
            return False

        try:
            f_size = os.path.getsize(video_path)
            log_step("upload_story.py", f"Starting upload ({f_size//1024} KB)", "info")

            start = self.base.session.post(
                f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
                data={"upload_phase": "start",
                      "file_size": f_size,
                      "access_token": page_token},
                timeout=30).json()
            v_id = start.get("video_id")
            v_url = start.get("upload_url")
            log_step("upload_story.py", f"Upload session: video_id={v_id}", "ok")

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

                log_step("upload_story.py", f"Video bytes sent", "ok",
                         f"HTTP {up_res.status_code}")

                if up_res.status_code in (200, 201):
                    finish = self.base.session.post(
                        f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
                        data={"upload_phase": "finish",
                              "video_id": v_id,
                              "access_token": page_token},
                        timeout=30).json()
                    if finish.get("success") or finish.get("post_id"):
                        self.base.api_status["Facebook Story"]["Upload"] = "success"
                        log_api("upload_story.py", "FB-Story-Finish", "success")
                        send_tg("✅ <b>Facebook Story LIVE!</b>")
                        return True

            self.base.api_status["Facebook Story"]["Upload"] = "failed"
            log_api("upload_story.py", "FB-Story", "failed")
            send_tg("❌ Facebook Story failed")
            return False
        except Exception as e:
            self.base.api_status["Facebook Story"]["Upload"] = f"failed ({str(e)[:40]})"
            log_api("upload_story.py", "FB-Story", "failed", str(e)[:100])
            send_tg(f"❌ Facebook Story: {str(e)[:120]}")
            return False
