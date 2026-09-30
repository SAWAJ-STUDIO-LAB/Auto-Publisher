import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from ..shared.telegram import send_tg

def upload_drive(path, prefix, folder_id=None, api_status=None):
    try:
        creds = Credentials(
            None, refresh_token=os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN"),
            client_id=os.environ.get("GOOGLE_DRIVE_CLIENT_ID"),
            client_secret=os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET"),
            token_uri="https://oauth2.googleapis.com/token"
        )
        service = build("drive", "v3", credentials=creds, cache_discovery=False)
        meta = {"name": f"{prefix}_{int(os.path.getmtime(path))}.mp4"}
        if folder_id: meta["parents"] = [folder_id]

        up = service.files().create(body=meta, media_body=MediaFileUpload(path, mimetype="video/mp4", resumable=True), fields="id").execute()
        did = up.get("id")
        service.permissions().create(fileId=did, body={"type": "anyone", "role": "reader"}).execute()
        link = f"https://drive.google.com/file/d/{did}/view"
        direct = f"https://drive.google.com/uc?export=download&id={did}"
        if api_status is not None: api_status["Drive"]["Google Drive"] = "success"
        send_tg(f"✅ Drive Link: {link}")
        return link, direct
    except Exception as e:
        if api_status is not None: api_status["Drive"]["Google Drive"] = f"failed ({str(e)[:50]})"
        send_tg(f"❌ Drive Error: {e}")
        return None, None
