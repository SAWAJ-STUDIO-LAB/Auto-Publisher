# ============================================================
# 📄 FILE:      E3_mastering.py
# 📁 PATH:      social_media/facebook/short_video/E_audio/E3_mastering.py
# 🎯 PURPOSE:   Audio mastering (normalize, tempo, volume)
# ============================================================

from A_core.A2_logger import log_file_start, log_file_end, log_step


# ─────────────────────────────────────────────────────────────
# ① MASTERING CLASS
# ─────────────────────────────────────────────────────────────
class Mastering:
    """Master voice audio (tempo + loudnorm + volume)."""

    # ─────────────────────────────────────────────────────────
    # ② INIT
    # ─────────────────────────────────────────────────────────
    def __init__(self, base):
        log_file_start("E3_mastering.py", "Audio mastering")
        self.base = base
        log_file_end("E3_mastering.py", "success", "Ready")

    # ─────────────────────────────────────────────────────────
    # ③ MASTER VOICE — apply tempo + loudnorm + volume
    # ─────────────────────────────────────────────────────────
    def master_voice(self, in_file, out_file):
        """
        Apply mastering:
          - Tempo: 0.88 (slower for clarity)
          - Loudnorm: I=-16 LUFS (broadcast standard)
          - Volume: 1.35x (boosted)
        """
        log_step("E3_mastering.py", "master_voice()", "ok")

        self.base.run_cmd(
            f'ffmpeg -y -i {in_file} -af '
            f'"atempo=0.88,loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.35" '
            f'{out_file}')

        return out_file
