"""
Central configuration loader.
Reads all env vars and exposes them as a Config object.
"""
import os
from dataclasses import dataclass, field


@dataclass
class Config:
    # Telegram
    tg_token: str = ""
    tg_chat_id: str = ""

    # GitHub
    github_token: str = ""

    # Drive
    drive_client_id: str = ""
    drive_client_secret: str = ""
    drive_refresh_token: str = ""
    drive_folder_id: str = ""

    # Meta
    meta_token: str = ""
    fb_page_id: str = ""
    ig_business_id: str = ""

    # AI
    openrouter_key: str = ""
    groq_key: str = ""
    gemini_key: str = ""
    mistral_key: str = ""
    cerebras_key: str = ""
    cohere_key: str = ""
    huggingface_key: str = ""

    # Media
    pexels_key: str = ""
    pixabay_key: str = ""
    freesound_key: str = ""
    elevenlabs_key: str = ""

    # Translation
    deepl_key: str = ""

    # Hadith
    hadith_api_url: str = ""

    # Runtime
    event_name: str = ""
    upload_to_social: bool = False

    @property
    def should_post_social(self) -> bool:
        """Auto-post on schedule, or manual run with tick."""
        return (self.event_name == "schedule") or self.upload_to_social


def load_config() -> Config:
    """Load config from environment variables."""
    cfg = Config(
        tg_token=os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        tg_chat_id=os.environ.get("TELEGRAM_CHAT_ID", ""),
        github_token=os.environ.get("TOKEN_GITHUB", ""),
        drive_client_id=os.environ.get("GOOGLE_DRIVE_CLIENT_ID", ""),
        drive_client_secret=os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET", ""),
        drive_refresh_token=os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN", ""),
        drive_folder_id=os.environ.get("DRIVE_STORY_FOLDER_ID", ""),
        meta_token=os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip(),
        fb_page_id=os.environ.get("FACEBOOK_PAGE_ID", "").strip(),
        ig_business_id=os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip(),
        openrouter_key=os.environ.get("OPENROUTER_API_KEY", ""),
        groq_key=os.environ.get("GROQ_API_KEY", ""),
        gemini_key=os.environ.get("GEMINI_API_KEY", ""),
        mistral_key=os.environ.get("MISTRAL_API_KEY", ""),
        cerebras_key=os.environ.get("CEREBRAS_API_KEY", ""),
        cohere_key=os.environ.get("COHERE_API_KEY", ""),
        huggingface_key=os.environ.get("HUGGINGFACE_API_KEY", ""),
        pexels_key=os.environ.get("PEXELS_API_KEY", ""),
        pixabay_key=os.environ.get("PIXABAY_API_KEY", ""),
        freesound_key=os.environ.get("FREESOUND_API_KEY", ""),
        elevenlabs_key=os.environ.get("ELEVENLABS_API_KEY", ""),
        deepl_key=os.environ.get("DEEPL_API_KEY", ""),
        hadith_api_url=os.environ.get("HADITH_API_URL", ""),
        event_name=os.environ.get("GITHUB_EVENT_NAME", ""),
        upload_to_social=str(os.environ.get("UPLOAD_TO_SOCIAL", "")).lower() == "true",
    )
    return cfg
