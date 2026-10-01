# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C9_meaning.py                             ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C9_meaning.py                   ║
# ║  🎯 PURPOSE:   ⭐ Detailed Hindi Meaning & Tashreeh      ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📖 DETAILED HINDI MEANING (TASHREEH) MODULE            ║
║   ═══════════════════════════════════════════            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Long video ke liye Hadith ka aasan Hindi Tarjuma    ║
║      aur Mufassal Tashreeh (Detailed Explanation)       ║
║      generate karna.                                     ║
╚══════════════════════════════════════════════════════════╝
"""

from C_content.C2_ai_provider import AIProvider
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class MeaningGenerator:
    """Generates extended Hindi explanation (Tashreeh) for 5-15 min videos."""

    def __init__(self, session=None):
        log_file_start("C9_meaning.py", "Init Meaning Generator")
        self.ai = AIProvider(session=session)
        log_file_end("C9_meaning.py", "success")

    def generate_extended_meaning(self, hadith_data: dict) -> dict:
        """Builds comprehensive Hindi Translation and detailed Explanation."""
        english = hadith_data.get("english", "")
        narrator = hadith_data.get("narrator", "")

        prompt = (
            f"Generate a detailed, beautiful, respectful Hindi Tashreeh (Explanation) for this Hadith narrated by {narrator}:\n"
            f"Text: {english}\n\n"
            "Include:\n"
            "1. Simple Hindi Tarjuma (Translation)\n"
            "2. Detailed Tashreeh (Explanation in 250-400 Hindi words)\n"
            "3. Life Lessons for Daily Routine\n\n"
            "Format cleanly with headings."
        )

        res = self.ai.generate(prompt, "You are a renowned Islamic scholar writing clear Hindi Tashreeh.")

        if not res:
            log_step("C9_meaning.py", "AI failed, using default fallback Tashreeh", "warn")
            res = (
                "इस हदीस का मफ़हूम यह है कि इंसान का हर अमल उसकी नियत पर निर्भर करता है। "
                "अल्लाह तआला सिर्फ़ ज़ाहिरी अमल नहीं देखता, बल्कि दिल का इख़लास और नियत देखता है। "
                "इसलिए हर नेक काम शुरू करने से पहले अपनी नियत सिर्फ़ अल्लाह की रज़ा के लिए ख़ालिस करें।"
            )

        log_step("C9_meaning.py", "Hindi Meaning Generated", "ok", f"{len(res.split())} words")
        return {
            "hindi_translation": res[:200] + "...",
            "full_tashreeh": res,
        }
