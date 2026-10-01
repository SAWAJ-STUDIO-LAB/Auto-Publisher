# ============================================================
# 📄 FILE:      D4_frames.py
# 📁 PATH:      social_media/facebook/story_video/D_video/D4_frames.py
# 🎯 PURPOSE:   Combine intro + main + outro into frames
# ⏱️  TIMING:   Intro 2s + Main 50-55s + Outro 2s = 54-59s total
# ============================================================

import os
from PIL import Image, ImageDraw
from A_core.A2_logger import log_file_start, log_file_end, log_step
from D_video.D1_intro import draw_intro
from D_video.D2_main_content import draw_main
from D_video.D3_outro import draw_outro


# ─────────────────────────────────────────────────────────────
# ① FRAMES CLASS
# ─────────────────────────────────────────────────────────────
class Frames:
    """Generate all frames — intro + main + outro."""

    # ─────────────────────────────────────────────────────────
    # ② INIT — set timing
    # ─────────────────────────────────────────────────────────
    def __init__(self):
        log_file_start("D4_frames.py", "Frame generation")
        self.fps = 25
        # TIMING: Intro 2s + Outro 2s = 4s total overlay
        self.intro_dur = 2.0
        self.outro_dur = 2.0
        log_file_end("D4_frames.py", "success",
                     f"Timing: {self.intro_dur}s intro + {self.outro_dur}s outro")

    # ─────────────────────────────────────────────────────────
    # ③ GENERATE — generate all frames
    # ─────────────────────────────────────────────────────────
    def generate(self, voice_dur, has_logo, hindi, urdu, english,
                 hadith_label="", out_dir="s_frames"):
        os.makedirs(out_dir, exist_ok=True)

        # Total = intro + voice + outro
        total = self.intro_dur + voice_dur + self.outro_dur

        log_step("D4_frames.py",
                 f"generate: intro={self.intro_dur}s + voice={voice_dur:.1f}s + outro={self.outro_dur}s = {total:.1f}s",
                 "ok")

        frames_count = int(total * self.fps)
        log_step("D4_frames.py", f"Generating {frames_count} frames", "info")

        for fi in range(frames_count):
            t = fi / self.fps
            img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            if t < self.intro_dur:
                # ═══════ INTRO ═══════
                draw_intro(img, draw, t, self.intro_dur, has_logo)
            elif t < self.intro_dur + voice_dur:
                # ═══════ MAIN ═══════
                mt = t - self.intro_dur
                draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
                          hadith_label, has_logo)
            else:
                # ═══════ OUTRO ═══════
                ot = t - (self.intro_dur + voice_dur)
                draw_outro(img, draw, ot, self.outro_dur, has_logo)

            img.save(f"{out_dir}/frame_{fi:05d}.png")

        log_step("D4_frames.py", "Frames done", "ok",
                 f"{frames_count} files in {out_dir}")
        return total
