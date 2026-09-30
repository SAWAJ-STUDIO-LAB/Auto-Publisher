"""ASS subtitle generator — word-by-word."""
from utils import sanitize
from logger import log_file_start, log_file_end, log_step


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

log_file_start("subtitles.py", "Word-by-word ASS subtitle generation")
log_file_end("subtitles.py", "success", "Ready")


def _ts(t):
    return f"0:{int(t // 60):02d}:{t % 60:05.2f}"


def _typed(text, style, start, end):
    words = sanitize(text).split()
    if not words:
        return ""
    wd = (end - start) / max(len(words), 1)
    out, t = "", start
    for w in words:
        out += f"Dialogue: 0,{_ts(t)},{_ts(t + wd)},{style},,0,0,0,,{w}\n"
        t += wd
    return out


def write_ass(arabic, hindi, english, dur, outfile="s_subs.ass"):
    log_step("subtitles.py", f"write_ass(dur={dur:.1f}s)", "ok")
    start = 1.4
    end = start + dur - 0.25
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER)
        ar_lines = _typed(arabic, "Arabic", start, end)
        hi_lines = _typed(hindi, "Hindi", start, end)
        en_lines = _typed(english, "English", start, end)
        f.write(ar_lines)
        f.write(hi_lines)
        f.write(en_lines)
    log_step("subtitles.py", f"ASS written: {outfile}", "ok",
             f"AR={len(ar_lines.splitlines())} HI={len(hi_lines.splitlines())} EN={len(en_lines.splitlines())}")
    return outfile
