# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E2_sfx.py                                 ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                E_audio/E2_sfx.py                         ║
# ║  🎯 PURPOSE:   Sound effects (whoosh, ding)              ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔊 SOUND EFFECTS MODULE                                ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Sound effects generate karna                        ║
║                                                          ║
║   📖 Functions:                                          ║
║      • whoosh_cmd()  → Transition whoosh sound           ║
║      • ding_cmd()    → CTA reveal ding sound             ║
║                                                          ║
║   📝 Note:                                                ║
║      Yeh functions FFmpeg commands return karti hain    ║
║      Directly run nahi karti                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝


# ═══════════════════════════════════════════════════════════
# 🔊 WHOOSH — soft whoosh for transitions
# ═══════════════════════════════════════════════════════════

def whoosh_cmd(outfile="whoosh.mp3"):
    """
    Return FFmpeg command for whoosh sound.

    Args:
        outfile: output mp3 path

    Returns:
        FFmpeg command string
    """
    return (f'ffmpeg -y -f lavfi -i "anoisesrc=d=0.5:c=pink:a=0.5" '
            f'-af "afade=t=in:d=0.1,afade=t=out:st=0.3:d=0.2,volume=0.3" '
            f'{outfile}')


# ═══════════════════════════════════════════════════════════
# 🔔 DING — soft bell for CTA reveal
# ═══════════════════════════════════════════════════════════

def ding_cmd(outfile="ding.mp3"):
    """
    Return FFmpeg command for ding sound.

    Args:
        outfile: output mp3 path

    Returns:
        FFmpeg command string
    """
    return (f'ffmpeg -y -f lavfi -i "sine=frequency=880:duration=0.5" '
            f'-af "afade=t=out:st=0.2:d=0.3,volume=0.4" '
            f'{outfile}')
