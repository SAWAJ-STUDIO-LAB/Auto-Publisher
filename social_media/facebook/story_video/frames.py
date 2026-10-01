"""Overlay frames generator — 3-language bullet display."""
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

    def _load_font(self, size, bold=True):
        paths = [
            os.path.expanduser("~/.fonts/NotoSansDevanagari-Bold.ttf" if bold else "~/.fonts/NotoSansDevanagari-Regular.ttf"),
            os.path.expanduser("~/.fonts/NotoNaskhArabic-Bold.ttf" if bold else "~/.fonts/NotoNaskhArabic-Regular.ttf"),
            os.path.expanduser("~/.fonts/NotoSans-Bold.ttf" if bold else "~/.fonts/NotoSans-Regular.ttf"),
        ]
        for p in paths:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
        return ImageFont.load_default()

    def _draw_text_centered(self, draw, text, y, font, fill, max_width=1000):
        """Draw text centered at given y, wrap if too wide."""
        if not text:
            return
        words = text.split()
        lines = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            x = (1080 - w) // 2
            # Shadow
            draw.text((x + 3, y + i * (font.size + 12) + 3), line,
                      fill=(0, 0, 0, 220), font=font)
            # Main
            draw.text((x, y + i * (font.size + 12)), line,
                      fill=fill, font=font)

    def _text_block_height(self, draw, text, font, max_width=1000):
        if not text:
            return 0
        words = text.split()
        lines = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return len(lines) * (font.size + 12)

    def generate(self, voice_dur, has_logo, hindi, urdu, english,
                 out_dir="s_frames"):
        os.makedirs(out_dir, exist_ok=True)
        log_step("frames.py", f"generate() dur={voice_dur:.1f}s", "ok",
                 f"logo={'yes' if has_logo else 'no'}")

        font_title = self._load_font(72, bold=True)
        font_lang = self._load_font(58, bold=True)

        logo_w, logo_h = 220, 95
        max_x, max_y = 1080 - logo_w, 1920 - logo_h
        total = self.intro + voice_dur + self.outro
        frames_count = int(total * self.fps)
        log_step("frames.py", f"Generating {frames_count} frames", "info")

        # Bullet colors (RGB)
        COLOR_HINDI = (240, 130, 200)     # Pink
        COLOR_URDU = (90, 170, 255)       # Blue
        COLOR_ENGLISH = (255, 100, 100)   # Red

        for fi in range(frames_count):
            t = fi / self.fps
            img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # === INTRO ===
            if t < self.intro:
                a = min(1.0, t / 0.5)
                self._draw_text_centered(draw, "SAWAJ STUDIO", 820,
                                         font_title,
                                         (220, 190, 120, int(255 * a)))
                self._draw_text_centered(draw, "Morning Story", 920,
                                         self._load_font(44, bold=False),
                                         (180, 160, 130, int(200 * a)))

            # === MAIN (bullet list of 3 languages) ===
            elif t < self.intro + voice_dur:
                mt = t - self.intro

                # Fade in first 0.6s
                alpha = min(1.0, mt / 0.6)

                # Calculate block start Y (center-ish)
                y_start = 820

                # Draw bullet + text for each language
                block_y = y_start

                # Hindi
                if hindi:
                    bbox = draw.textbbox((0, 0), hindi, font=font_lang)
                    tw = bbox[2] - bbox[0]
                    # bullet circle
                    draw.ellipse([120, block_y + 22, 152, block_y + 54],
                                 fill=(*COLOR_HINDI, int(255 * alpha)))
                    # text (with shadow)
                    tx = 180
                    draw.text((tx + 3, block_y + 3), hindi,
                              fill=(0, 0, 0, int(220 * alpha)), font=font_lang)
                    draw.text((tx, block_y), hindi,
                              fill=(*COLOR_HINDI, int(255 * alpha)), font=font_lang)
                    block_y += 110

                # Urdu / Arabic
                if urdu:
                    bbox = draw.textbbox((0, 0), urdu, font=font_lang)
                    tw = bbox[2] - bbox[0]
                    draw.ellipse([120, block_y + 22, 152, block_y + 54],
                                 fill=(*COLOR_URDU, int(255 * alpha)))
                    tx = 180
                    draw.text((tx + 3, block_y + 3), urdu,
                              fill=(0, 0, 0, int(220 * alpha)), font=font_lang)
                    draw.text((tx, block_y), urdu,
                              fill=(*COLOR_URDU, int(255 * alpha)), font=font_lang)
                    block_y += 110

                # English
                if english:
                    bbox = draw.textbbox((0, 0), english, font=font_lang)
                    tw = bbox[2] - bbox[0]
                    draw.ellipse([120, block_y + 22, 152, block_y + 54],
                                 fill=(*COLOR_ENGLISH, int(255 * alpha)))
                    tx = 180
                    draw.text((tx + 3, block_y + 3), english,
                              fill=(0, 0, 0, int(220 * alpha)), font=font_lang)
                    draw.text((tx, block_y), english,
                              fill=(*COLOR_ENGLISH, int(255 * alpha)), font=font_lang)

                # Floating logo
                if has_logo:
                    try:
                        logo = Image.open("avatar.png").convert("RGBA").resize(
                            (logo_w, logo_h), Image.Resampling.LANCZOS)
                        x = abs((int(mt * 200) + 60) % (2 * max_x) - max_x)
                        y = abs((int(mt * 150) + 120) % (2 * max_y) - max_y)
                        img.paste(logo, (x, y), logo)
                    except Exception:
                        pass

            # === OUTRO ===
            else:
                ot = t - (self.intro + voice_dur)
                a = min(1.0, ot / 0.55)
                self._draw_text_centered(draw, "JazakAllah Khair", 860,
                                         font_title,
                                         (220, 190, 120, int(255 * a)))
                if has_logo:
                    try:
                        logo = Image.open("avatar.png").convert("RGBA").resize(
                            (190, 80), Image.Resampling.LANCZOS)
                        img.paste(logo, (445, 970), logo)
                    except Exception:
                        pass

            img.save(f"{out_dir}/frame_{fi:05d}.png")

        log_step("frames.py", "Frames done", "ok",
                 f"{frames_count} files in {out_dir}")
        return total
