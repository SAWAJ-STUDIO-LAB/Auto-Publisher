"""Config — reads env variables."""
import os
from logger import log_file_start, log_file_end, log_step


class Config:
    log_file_start("config.py", "Load environment variables")

    TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

    META_TOKEN = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
    PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

    DRIVE_CLIENT_ID = os.environ.get("GOOGLE_DRIVE_CLIENT_ID")
    DRIVE_CLIENT_SECRET = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET")
    DRIVE_REFRESH_TOKEN = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN")
    DRIVE_STORY_FOLDER_ID = os.environ.get("DRIVE_STORY_FOLDER_ID")

    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
    CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY")
    COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
    HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")

    PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
    PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY")
    FREESOUND_API_KEY = os.environ.get("FREESOUND_API_KEY")

    HADITH_API_URL = os.environ.get("HADITH_API_URL")

    EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME", "")
    UPLOAD_TO_SOCIAL = str(os.environ.get("UPLOAD_TO_SOCIAL", "")).lower() == "true"

    @property
    def should_post_social(self):
        return (self.EVENT_NAME == "schedule") or self.UPLOAD_TO_SOCIAL


def _check_env():
    checks = [
        ("Telegram Token", Config.TG_TOKEN),
        ("Telegram Chat ID", Config.TG_CHAT_ID),
        ("Facebook Meta Token", Config.META_TOKEN),
        ("Facebook Page ID", Config.PAGE_ID),
        ("Google Drive Refresh", Config.DRIVE_REFRESH_TOKEN),
        ("At least 1 AI Key", any([
            Config.OPENROUTER_API_KEY, Config.GROQ_API_KEY,
            Config.GEMINI_API_KEY, Config.MISTRAL_API_KEY,
            Config.CEREBRAS_API_KEY, Config.COHERE_API_KEY,
        ])),
        ("ElevenLabs Key", Config.ELEVENLABS_API_KEY),
        ("Pexels Key", Config.PEXELS_API_KEY),
    ]
    for name, val in checks:
        if val:
            log_step("config.py", f"ENV: {name}", "ok", "present")
        else:
            log_step("config.py", f"ENV: {name}", "warn", "missing (fallback)")

    log_step("config.py", "should_post_social", "info",
             str(Config().should_post_social))
    log_file_end("config.py", "success", "Config loaded")


_check_env()
