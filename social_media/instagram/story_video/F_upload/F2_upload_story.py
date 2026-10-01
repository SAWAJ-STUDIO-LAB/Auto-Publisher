import os
import time
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class StoryUploader:
    def __init__(self, base):
        log_file_start("F2_upload_story.py", "IG Story upload")
        self.base = base
        log_file_end("F2_upload_story.py", "success", "Ready")

    def upload(self, video_path):
        log_step("F2_upload_story.py", "upload()", "ok")
        token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
        ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
        if not token or not ig_id:
            log_step("F2_upload_story.py", "Missing creds", "fail")
            return False
        try:
            cont = self.base.session.post(
                f"https://graph.facebook.com/v21.0/{ig_id}/media",
                data={"media_type": "STORIES", "upload_type": "resumable", "access_token": token},
                timeout=40).json()
            c_id = cont.get("id")
            if not c_id:
                log_api("F2_upload_story.py", "IG-Container", "failed")
                return False
            upload_url = cont.get("uri") or f"https://rupload.facebook.com/ig-api-upload/v21.0/{c_id}"
            f_size = os.path.getsize(video_path)
            with open(video_path, "rb") as f:
                vbytes = f.read()
            headers = {"Authorization": f"OAuth {token}", "offset": "0", "file_size": str(f_size), "Content-Type": "application/octet-stream"}
            self.base.session.post(upload_url, headers=headers, data=vbytes, timeout=180)
            for _ in range(40):
                time.sleep(5)
                st = self.base.session.get(
                    f"https://graph.facebook.com/v21.0/{c_id}",
                    params={"fields": "status_code", "access_token": token}, timeout=15).json()
                if st.get("status_code") == "FINISHED":
                    pub = self.base.session.post(
                        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
                        data={"creation_id": c_id, "access_token": token}, timeout=20).json()
                    if pub.get("id"):
                        self.base.api_status["Instagram Story"]["Upload"] = "success"
                        log_api("F2_upload_story.py", "IG-Story", "success", pub["id"])
                        return True
                    break
                if st.get("status_code") == "ERROR":
                    break
            log_api("F2_upload_story.py", "IG-Story", "failed")
            return False
        except Exception as e:
            log_api("F2_upload_story.py", "IG-Story", "failed", str(e)[:100])
            return False
