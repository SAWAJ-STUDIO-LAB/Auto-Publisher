"""Overlay frames generator."""
import os
from PIL import Image, ImageDraw, ImageFont
from logger import log_file_start, log_file_end, log_step


class Frames:
    def __init__(self):
        log_file_start("frames.py", "Frame-by-frame overlay generation")
        self.fps = 25
        self.intro = 1.5
        self.outro = 1.7
        log_file_end("frames.py", "success", "Ready")

    def generate(self, voice_dur, has_logo, out_dir="s_frames"):
        os.makedirs(out_dir, exist_ok=True)
        log_step("frames.py", f"generate() dur={voice_dur:.1f}s", "ok",
                 f"logo={'yes' if has_logo else 'no'}")

        try:
            font_big = ImageFont.truetype(
                os.path.expanduser("~/.fonts/NotoSans-Bold.ttf"), 68)
            font_s = ImageFont.truetype(
                os.path.expanduser("~/.fonts/NotoSans-Bold.ttf"), 42)
        except Exception:
            log_step("frames.py", "Font fallback to default", "warn")
            font_big = font_s = ImageFont.load_default()

        logo_w, logo_h = 220, 95
        max_x, max_y = 1080 - logo_w, 1920 - logo_h
        total = self.intro + voice_dur + self.outro

        frames_count = int(total * self.fps)
        log_step("frames.py", f"Generating {frames_count} frames", "info")

        for fi in range(frames_count):
            t = fi / self.fps
            img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            if t < self.intro:
                a = min(1.0, t / 0.5)
                draw.text((540, 870), "SAWAJ STUDIO",
                          fill=(220, 190, 120, int(255 * a)),
                          font=font_big, anchor="mm")
                draw.text((540, 960), "Morning Story",
                          fill=(180, 160, 130, int(200 * a)),
                          font=font_s, anchor="mm")
            elif t < self.intro + voice_dur:
                mt = t - self.intro
                if has_logo:
                    try:
                        logo = Image.open("avatar.png").convert("RGBA").resize(
                            (logo_w, logo_h), Image.Resampling.LANCZOS)
                        x = abs((int(mt * 200) + 60) % (2 * max_x) - max_x)
                        y = abs((int(mt * 150) + 120) % (2 * max_y) - max_y)
                        img.paste(logo, (x, y), logo)
                    except Exception:
                        pass
            else:
                ot = t - (self.intro + voice_dur)
                a = min(1.0, ot / 0.55)
                draw.text((540, 860), "JazakAllah Khair",
                          fill=(220, 190, 120, int(255 * a)),
                          font=font_big, anchor="mm")
                if has_logo:
                    try:
                        logo = Image.open("avatar.png").convert("RGBA").resize(
                            (190, 80), Image.Resampling.LANCZOS)
                        img.paste(logo, (445, 970), logo)
                    except Exception:
                        pass
            img.save(f"{out_dir}/frame_{fi:05d}.png")

        log_step("frames.py", f"Frames done", "ok",
                 f"{frames_count} files in {out_dir}")
        return total
