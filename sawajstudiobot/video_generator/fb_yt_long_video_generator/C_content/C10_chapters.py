# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C10_chapters.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C10_chapters.py                 ║
# ║  🎯 PURPOSE:   ⭐ YouTube Chapters & Timestamps Generator ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🏷️ YOUTUBE CHAPTERS & TIMESTAMPS MODULE                ║
║   ═══════════════════════════════════════                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Long Video ke timeline ke hisab se automatic        ║
║      YouTube Chapters (00:00 Intro, 00:30 Recitation...) ║
║      aur video description format generate karna.        ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step


class ChapterGenerator:
    """Calculates timestamps and generates chapter markers for YouTube videos."""

    @staticmethod
    def build_chapters(section_durations: dict) -> list:
        """
        section_durations = {
            "Intro / Bismillah": 25.0,
            "Arabic Recitation": 60.0,
            "Hindi Tarjuma": 90.0,
            "Detailed Tashreeh": 180.0,
            "Key Lessons": 45.0,
            "JazakAllah Outro": 20.0
        }
        Returns list of dicts with formatted timestamp & chapter name.
        """
        log_file_start("C10_chapters.py", "Build YouTube Chapters")
        chapters = []
        current_time = 0.0

        for title, duration in section_durations.items():
            mins = int(current_time // 60)
            secs = int(current_time % 60)
            time_str = f"{mins:02d}:{secs:02d}"

            chapters.append({
                "time_str": time_str,
                "seconds": current_time,
                "title": title
            })
            current_time += duration

        log_file_end("C10_chapters.py", "success", f"Created {len(chapters)} chapters")
        return chapters

    @staticmethod
    def format_description_chapters(chapters: list) -> str:
        """Formats list into YouTube description timestamp block."""
        lines = ["📌 Timestamps / Chapters:"]
        for c in chapters:
            lines.append(f"{c['time_str']} - {c['title']}")
        return "\n".join(lines)
