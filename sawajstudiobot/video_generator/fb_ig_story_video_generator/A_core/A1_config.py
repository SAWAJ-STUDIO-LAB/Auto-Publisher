# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A1_config.py                              ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                A_core/A1_config.py                       ║
# ║  🎯 PURPOSE:   Load all environment variables            ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   ⚙️  CONFIG MODULE                                       ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Saare environment variables ek jagah load karna    ║
║                                                          ║
║   📖 Usage:                                              ║
║      from A_core.A1_config import Config                 ║
║      cfg = Config()                                      ║
║      print(cfg.PAGE_ID)                                  ║
║                                                          ║
║   🔐 Secrets:                                            ║
║      GitHub Secrets se automatically load hote hain     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os


# ═══════════════════════════════════════════════════════════
# 🎯 CONFIG CLASS
# ═══════════════════════════════════════════════════════════

class Config:
    """
    Central Config — reads all env variables once.

    Saare API keys, tokens, aur settings yeh class provide karti hai.
    Har file `from A_core.A1_config import Config` se import karti hai.
    """

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
    # ③ INSTAGRAM
    # ─────────────────────────────────────────────────────
    IG_TOKEN = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    IG_BUSINESS_ID = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()

    # ─────────────────────────────────────────────────────
    # ④ GOOGLE DRIVE
    # ─────────────────────────────────────────────────────
    DRIVE_CLIENT_ID = os.environ.get("GOOGLE_DRIVE_CLIENT_ID")
    DRIVE_CLIENT_SECRET = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET")
    DRIVE_REFRESH_TOKEN = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN")
    DRIVE_STORY_FOLDER_ID = os.environ.get("GDRIVE_STORY_VIDEO_FOLDER_ID")

    # ─────────────────────────────────────────────────────
    # ⑤ AI PROVIDERS (Multi-Fallback)
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

    # ─────────────────────────────────────────────────────
    # ⑩ PROPERTY: should_post_social
    # ─────────────────────────────────────────────────────
    @property
    def should_post_social(self):
        """
        Returns True if:
          - Scheduled run (cron), OR
          - Manual run with upload_to_social = true
        """
        return (self.EVENT_NAME == "schedule") or self.UPLOAD_TO_SOCIAL
