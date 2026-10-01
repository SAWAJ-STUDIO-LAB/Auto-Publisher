# ============================================================
# 📄 FILE:      F1_drive.py
# 📁 PATH:      social_media/facebook/short_video/F_upload/F1_drive.py
# 🎯 PURPOSE:   Google Drive upload (backup)
# ============================================================

import os
import time
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


# ─────────────────────────────────────────────────────────────
# ① DRIVE CLASS
# ─────────────────────────────────────────────────────────────
class Drive:
    """Upload video to Google Drive."""

    # ─────────────────────────────────────────────────────────
    # ② INIT
    # ─────────────────────────────────────────────────────────
    def __init__(self, base):
        log_file_start("F1_drive.py", "Google Drive upload")
        self.base = base
        log_file_end("F1_drive.py", "success", "Ready")

    # ─────────────────────────────────────────────────────────
    # ③ UPLOAD — upload video to Drive
    # ─────────────────────────────────────────────────────────
    def upload(self, path, prefix="Short"):
        log_step("F1_drive.py", f"upload({path})", "ok")
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload

            # ───────── Authenticate ─────────
            creds = Credentials(
                None,
                refresh_token=os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN"),
                client_id=os.environ.get("GOOGLE_DRIVE_CLIENT_ID"),
                client_secret=os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET"),
                token_uri="https://oauth2.googleapis.com/token")
            service = build("drive", "v3", credentials=creds, cache_discovery=False)

            # ───────── Prepare metadata ─────────
            meta = {"name": f"{prefix}_{int(time.time())}.mp4"}
            folder_id = os.environ.get("DRIVE_FOLDER_ID")
            if folder_id:
                meta["parents"] = [folder_id]

            # ───────── Upload ─────────
            up = service.files().create(
                body=meta,
                media_body=MediaFileUpload(path, mimetype="video/mp4", resumable=True),
                fields="id").execute()
            did = up.get("id")

            # ───────── Make public ─────────
            service.permissions().create(
                fileId=did,
                body={"type": "anyone", "role": "reader"}).execute()

            link = f"https://drive.google.com/file/d/{did}/view"
            direct = f"https://drive.google.com/uc?export=download&id={did}"

            self.base.api_status["Drive"]["Google Drive"] = "success"
            log_api("F1_drive.py", "Google Drive", "success", did)
            return link, direct
        except Exception as e:
            self.base.api_status["Drive"]["Google Drive"] = f"failed ({str(e)[:50]})"
            log_api("F1_drive.py", "Google Drive", "failed", str(e)[:100])
            return None, None
