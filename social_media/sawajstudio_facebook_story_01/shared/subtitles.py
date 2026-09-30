"""
ASS subtitle generator — Arabic + Hindi + English styles,
word-by-word "typed" animation.
"""
from shared.utils import sanitize
from shared.logger import get_logger

logger = get_logger("subtitles")

ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Arabic,Noto Naskh Arabic,86,&H00F0E6D2,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,2,40,40,140,1
Style: Hindi,Noto Sans Devanagari,72,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,40,40,420,1
Style: English,Noto Sans,58,&H00D0D0D0,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,40,40,620,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""


def _ts(t: float) -> str:
    return f"0:{int(t // 60):02d}:{t % 60:05.2f}"


def _typed(text: str, style: str, start: float, end: float) -> str:
    """Word-by-word reveal."""
    words = sanitize(text).split()
    if not words:
        return ""
    wd = (end - start) / max(len(words), 1)
    out, t = "", start
    for w in words:
        out += f"Dialogue: 0,{_ts(t)},{_ts(t + wd)},{style},,0,0,0,,{w}\n"
        t += wd
    return out


def build_story_ass(
    hadith: dict,
    hindi: str,
    d1: float,
    outfile: str = "s_subs.ass",
) -> str:
    """Build story-style ASS file. Returns filename."""
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER)
        f.write(_typed(hadith.get("arabic", ""), "Arabic", 1.4, 1.4 + d1 - 0.25))
        f.write(_typed(hindi, "Hindi", 1.4, 1.4 + d1 - 0.25))
        f.write(_typed(hadith["english"], "English", 1.4, 1.4 + d1 - 0.25))
    logger.info(f"Subtitles written → {outfile}")
    return outfile
