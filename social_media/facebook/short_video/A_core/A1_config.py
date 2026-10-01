import os

class Config:
    TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    META_TOKEN = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
    PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    DRIVE_CLIENT_ID = os.environ.get("GOOGLE_DRIVE_CLIENT_ID")
    DRIVE_CLIENT_SECRET = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET")
    DRIVE_REFRESH_TOKEN = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN")
    DRIVE_FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID")
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
