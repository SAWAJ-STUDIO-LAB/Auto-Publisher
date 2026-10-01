import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class ShortUploader:
    def __init__(self, base):
        log_file_start("F2_upload_short.py", "YT upload")
        self.base = base
        log_file_end("F2_upload_short.py", "success", "Ready")

    def upload(self, video_path, title="", description="", tags=None):
        log_step("F2_upload_short.py", "upload()", "ok")
        try:
  from google.oauth2.credentials import Credentials
  from googleapiclient.discovery import build
  from googleapiclient.http import MediaFileUpload
  creds = Credentials(
      None,
      refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"),
      client_id=os.environ.get("YOUTUBE_CLIENT_ID"),
      client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET"),
      token_uri="https://oauth2.googleapis.com/token")
  yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
  body = {
      "snippet": {"title": title[:100], "description": description,
                  "tags": tags or ["Shorts", "Hadith"], "categoryId": "22"},
      "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
  }
  req = yt.videos().insert(part="snippet,status", body=body,
                           media_body=MediaFileUpload(video_path, chunksize=-1,
                                                      resumable=True, mimetype="video/mp4"))
  resp = None
  while resp is None:
      _, resp = req.next_chunk()
  vid = resp.get("id")
  self.base.api_status["YouTube"]["Upload"] = "success"
  log_api("F2_upload_short.py", "YT", "success", vid)
  pl = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID")
  if vid and pl:
      try:
          yt.playlistItems().insert(
              part="snippet",
              body={"snippet": {"playlistId": pl.strip(),
                                "resourceId": {"kind": "youtube#video", "videoId": vid}}}
          ).execute()
      except Exception:
          pass
  return True
        except Exception as e:
  log_api("F2_upload_short.py", "YT", "failed", str(e)[:100])
  return False
