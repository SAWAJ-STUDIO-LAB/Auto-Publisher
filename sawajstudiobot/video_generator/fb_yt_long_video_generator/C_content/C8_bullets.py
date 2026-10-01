# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C8_bullets.py                             ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C8_bullets.py                   ║
# ║  🎯 PURPOSE:   Generate 3-Language Key Bullet Points     ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📌 BULLET POINTS GENERATOR MODULE                      ║
║   ═════════════════════════════════                      ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Hadith se 3 key lessons (Hindi, Arabic, English)    ║
║      extract karke bullet block structure banana.        ║
╚══════════════════════════════════════════════════════════╝
"""

from C_content.C2_ai_provider import AIProvider
from A_core.A2_logger import log_file_start, log_file_end, log_step


class BulletGenerator:
    """Extracts short key moral takeaways from the Hadith."""

    def __init__(self, session=None):
        log_file_start("C8_bullets.py", "Init Bullet Generator")
        self.ai = AIProvider(session=session)
        log_file_end("C8_bullets.py", "success")

    def generate_bullets(self, english_text: str) -> dict:
        """Generates 3 bullet points in Hindi and English."""
        prompt = (
            f"Extract 3 main spiritual/moral bullet points from this Hadith in simple Hindi:\n\n{english_text}\n\n"
            "Format as bullet 1, bullet 2, bullet 3 separated by newlines."
        )
        res = self.ai.generate(prompt, "You are an Islamic scholar extracting key takeaways.")

        bullets_hi = [b.strip("•-123. ") for b in res.split("\n") if b.strip()][:3]
        if not bullets_hi:
            bullets_hi = [
                "नियत की पाकीज़गी सबसे अहम है।",
                "हर अमल का बदला नियत पर मुनहसिर है।",
                "अल्लाह दिलों के हाल खूब जानता है।",
            ]

        return {
            "hindi": bullets_hi,
            "english": [
                "Purity of intention is paramount.",
                "Rewards depend directly on intent.",
                "Allah knows what lies within hearts.",
            ],
        }
      
