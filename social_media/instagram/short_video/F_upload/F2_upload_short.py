import os
import time
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class ShortUploader:
    def __init__(self, base):
        log_file_start("F2_upload_short.py", "IG Reel upload")
        self.base = base
        log_file_end("F2_upload_short.py", "success", "Ready")

    def upload(self, video_path, caption="", direct_url=None):
        log_step("F2_upload_short.py", "upload()", "ok")
        token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
        ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
        if not token or not ig_id or not direct_url:
  log_step("F2_upload_short.py", "Missing creds/url", "fail")
  return False
        try:
  cont = self.base.session.post(
      f"https://graph.facebook.com/v21.0/{ig_id}/media",
      data={"media_type": "REELS", "video_url": direct_url, "caption": caption, "access_token": token},
      timeout=30).json()
  cid = cont.get("id")
  if not cid:
      log_api("F2_upload_short.py", "IG-Container", "failed")
      return False
  for _ in range(45):
      time.sleep(6)
      st = self.base.session.get(
          f"https://graph.facebook.com/v21.0/{cid}",
          params={"fields": "status_code", "access_token": token}, timeout=12).json()
      if st.get("status_code") == "FINISHED":
          break
      if st.get("status_code") == "ERROR":
          return False
  pub = self.base.session.post(
      f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
      data={"creation_id": cid, "access_token": token}, timeout=18).json()
  if pub.get("id"):
      self.base.api_status["Instagram"]["Reel"] = "success"
      log_api("F2_upload_short.py", "IG-Reel", "success", pub["id"])
      return True
  log_api("F2_upload_short.py", "IG-Reel", "failed")
  return False
        except Exception as e:
  log_api("F2_upload_short.py", "IG-Reel", "failed", str(e)[:100])
  return False
