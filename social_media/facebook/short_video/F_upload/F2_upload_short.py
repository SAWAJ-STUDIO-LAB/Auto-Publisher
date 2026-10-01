import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class ShortUploader:
    def __init__(self, base):
        log_file_start("F2_upload_short.py", "FB upload")
        self.base = base
        log_file_end("F2_upload_short.py", "success", "Ready")

    def upload(self, video_path, caption=""):
        log_step("F2_upload_short.py", "upload()", "ok")
        token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
        if not token or not page_id:
  log_step("F2_upload_short.py", "Missing creds", "fail")
  return False
        try:
  with open(video_path, "rb") as f:
      res = self.base.session.post(
          f"https://graph.facebook.com/v21.0/{page_id}/videos",
          data={"access_token": token, "description": caption, "published": "true"},
          files={"source": f}, timeout=400).json()
  if res.get("id"):
      self.base.api_status["Facebook"]["Upload"] = "success"
      log_api("F2_upload_short.py", "FB", "success", res["id"])
      return True
  log_api("F2_upload_short.py", "FB", "failed", str(res)[:100])
  return False
        except Exception as e:
  log_api("F2_upload_short.py", "FB", "failed", str(e)[:100])
  return False
