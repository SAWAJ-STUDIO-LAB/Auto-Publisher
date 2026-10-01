# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A1_config.py                              ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                A_core/A1_config.py                       ║
# ║  🎯 PURPOSE:   Load all environment variables            ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   ⚙️  CONFIG MODULE (LONG)                                ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Saare environment variables ek jagah load karna    ║
║                                                          ║
║   📝 Difference from Story:                               ║
║      • YT config (Short mein tha)                        ║
║      • Long video folder ID                              ║
║      • IG nahi hai (Long IG par nahi jata)              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os


class Config:
    """Central Config — reads all env variables once (Long)."""

    # ─────────────────────────────────────────────────────
    # ① TELEGRAM
    # ─────────────────────────────────────────────────────
    TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

    # ─────────────────────────────────────────────────────
    # ② FACEBOOK / META
    # ─────────────────────────────────────────────────────
    META_TOKEN = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
    PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

    # ─────────────────────────────────────────────────────
    # ③ YOUTUBE
    # ─────────────────────────────────────────────────────
    YT_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
    YT_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
    YT_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    YT_PLAYLIST_ID = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID")

    # ─────────────────────────────────────────────────────
    # ④ GOOGLE DRIVE
    # ─────────────────────────────────────────────────────
    DRIVE_CLIENT_ID = os.environ.get("GOOGLE_DRIVE_CLIENT_ID")
    DRIVE_CLIENT_SECRET = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET")
    DRIVE_REFRESH_TOKEN = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN")
    DRIVE_LONG_FOLDER_ID = os.environ.get("GDRIVE_LONG_VIDEO_FOLDER_ID")

    # ─────────────────────────────────────────────────────
    # ⑤ AI PROVIDERS
    # ─────────────────────────────────────────────────────
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
    CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY")
    COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
    HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

    # ─────────────────────────────────────────────────────
    # ⑥ TTS / TRANSLATION
    # ─────────────────────────────────────────────────────
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")

    # ─────────────────────────────────────────────────────
    # ⑦ MEDIA APIS
    # ─────────────────────────────────────────────────────
    PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
    PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY")
    FREESOUND_API_KEY = os.environ.get("FREESOUND_API_KEY")

    # ─────────────────────────────────────────────────────
    # ⑧ HADITH API
    # ─────────────────────────────────────────────────────
    HADITH_API_URL = os.environ.get("HADITH_API_URL")

    # ─────────────────────────────────────────────────────
    # ⑨ RUNTIME
    # ─────────────────────────────────────────────────────
    EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME", "")
    UPLOAD_TO_SOCIAL = str(os.environ.get("UPLOAD_TO_SOCIAL", "")).lower() == "true"
    PLATFORM = os.environ.get("PLATFORM", "facebook")

    @property
    def should_post_social(self):
        """True if scheduled OR manual with upload flag."""
        return (self.EVENT_NAME == "schedule") or self.UPLOAD_TO_SOCIAL
