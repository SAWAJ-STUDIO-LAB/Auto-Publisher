# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C7_subtitles.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C7_subtitles.py                 ║
# ║  🎯 PURPOSE:   SRT Subtitle File Generator               ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📜 SUBTITLE GENERATOR MODULE                           ║
║   ════════════════════════════                           ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Generates timed .srt files for YouTube & Facebook   ║
║      closed captions support.                            ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step


def format_timestamp(seconds: float) -> str:
    """Formats float seconds into SRT timestamp HH:MM:SS,mmm."""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"


class SubtitleGenerator:
    """Builds SRT files for long video captions."""

    @staticmethod
    def create_srt(segments: list, output_srt_path: str) -> bool:
        """
        segments = [{"start": 0.0, "end": 5.2, "text": "In the name of Allah..."}, ...]
        """
        log_file_start("C7_subtitles.py", "Generate SRT")
        if not segments:
            log_step("C7_subtitles.py", "No segments provided", "warn")
            return False

        try:
            with open(output_srt_path, "w", encoding="utf-8") as f:
                for idx, seg in enumerate(segments, 1):
                    start_str = format_timestamp(seg.get("start", 0.0))
                    end_str = format_timestamp(seg.get("end", 0.0))
                    text = seg.get("text", "").strip()

                    f.write(f"{idx}\n")
                    f.write(f"{start_str} --> {end_str}\n")
                    f.write(f"{text}\n\n")

            log_file_end("C7_subtitles.py", "success", f"Saved {len(segments)} blocks")
            return True
        except Exception as e:
            log_step("C7_subtitles.py", "Failed to write SRT", "fail", str(e)[:60])
            return False
          
