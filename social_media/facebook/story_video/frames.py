"""Overlay frames generator — INTRO + 3-Language MAIN + OUTRO + Effects."""
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from logger import log_file_start, log_file_end, log_step


class Frames:
    def __init__(self):
        log_file_start("frames.py", "Frame-by-frame overlay generation")
        self.fps = 25
        self.intro = 2.5
        self.outro = 3.0
        log_file_end("frames.py", "success", "Ready")

    # ---------- Font loader ----------
    def _load_font(self, size, script="latin", bold=True):
        paths = []
        if script == "devanagari":
            paths = [
                "~/.fonts/NotoSansDevanagari-Bold.ttf" if bold
                else "~/.fonts/NotoSansDevanagari-Regular.ttf",
            ]
        elif script == "arabic":
            paths = [
                "~/.fonts/NotoNaskhArabic-Bold.ttf" if bold
                else "~/.fonts/NotoNaskhArabic-Regular.ttf",
            ]
        else:
            paths = [
                "~/.fonts/NotoSans-Bold.ttf" if bold
                else "~/.fonts/NotoSans-Regular.ttf",
            ]
        for p in paths:
            try:
                return ImageFont.truetype(os.path.expanduser(p), size)
            except Exception:
                continue
        return ImageFont.load_default()

    # ---------- Text centering helper ----------
    def _draw_text_centered(self, draw, text, y, font, fill,
                            shadow=True, max_width=1000):
        if not text:
            return
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = (1080 - w) // 2
        if shadow:
            draw.text((x + 4, y + 4), text,
                      fill=(0, 0, 0, 220), font=font)
        draw.text((x, y), text, fill=fill, font=font)

    # ---------- Sparkles ----------
    def _draw_sparkles(self, draw, t):
        rng = random.Random(int(t * 10))
        for _ in range(12):
            x = rng.randint(80, 1000)
            y = rng.randint(200, 1800)
            size = rng.randint(3, 9)
            alpha = int(120 + 100 * math.sin(t * 3 + x))
            alpha = max(50, min(255, alpha))
            draw.ellipse([x - size, y - size, x + size, y + size],
                         fill=(255, 240, 180, alpha))

    # ---------- Progress bar ----------
    def _draw_progress(self, draw, current, total, y=1820):
        bar_x = 80
        bar_w = 920
        bar_h = 8
        # Track
        draw.rectangle([bar_x, y, bar_x + bar_w, y + bar_h],
                       fill=(0, 0, 0, 150))
        # Fill
        pct = min(1.0, current / max(total, 1))
        fill_w = int(bar_w * pct)
        draw.rectangle([bar_x, y, bar_x + fill_w, y + bar_h],
                       fill=(212, 175, 55, 255))
        # Glow dot at end
        if fill_w > 0:
            gx = bar_x + fill_w
            draw.ellipse([gx - 8, y - 4, gx + 8, y + 12],
                         fill=(255, 220, 120, 220))

    # ---------- Hadith number badge ----------
    def _draw_badge(self, draw, text, y=180):
        try:
            fnt = self._load_font(26, "latin", bold=True)
        except Exception:
            fnt = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=fnt)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        pad = 12
        x1 = 60
        y1 = y
        x2 = x1 + w + pad * 2
        y2 = y1 + h + pad
        # Background
        draw.rounded_rectangle([x1, y1, x2, y2], radius=8,
                               fill=(20, 15, 8, 200),
                               outline=(212, 175, 55, 220), width=2)
        draw.text((x1 + pad, y1 + pad // 2), text,
                  fill=(230, 200, 130, 255), font=fnt)

    # ---------- Main generate ----------
    def generate(self, voice_dur, has_logo, hindi, urdu, english,
                 hadith_label="", out_dir="s_frames"):
        os.makedirs(out_dir, exist_ok=True)
        log_step("frames.py", f"generate() dur={voice_dur:.1f}s", "ok",
                 f"logo={'yes' if has_logo else 'no'}")

        font_title = self._load_font(76, "latin", bold=True)
        font_sub = self._load_font(40, "latin", bold=False)
        font_lang = self._load_font(56, "latin", bold=True)
        font_hindi = self._load_font(56, "devanagari", bold=True)
        font_arabic = self._load_font(56, "arabic", bold=True)
        font_outro = self._load_font(72, "latin", bold=True)
        font_cta = self._load_font(44, "latin", bold=True)

        logo_w, logo_h = 240, 100
        max_x = 1080 - logo_w
        max_y = 1920 - logo_h
        total = self.intro + voice_dur + self.outro
        frames_count = int(total * self.fps)
        log_step("frames.py", f"Generating {frames_count} frames", "info")

        # Colors
        C_HINDI = (240, 130, 200)
        C_URDU = (90, 170, 255)
        C_ENGLISH = (255, 110, 110)
        C_GOLD = (230, 200, 130)

        for fi in range(frames_count):
            t = fi / self.fps
            img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # ==============================
            # INTRO (0 → 2.5s)
            # ==============================
            if t < self.intro:
                p = t / self.intro  # 0 to 1
                alpha = min(1.0, t / 0.5)

                # Bismillah fading in from top
                self._draw_text_centered(
                    draw, "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ",
                    200, font_arabic,
                    (230, 200, 130, int(255 * alpha)))

                # Gold line sweep
                line_y = 320
                line_progress = min(1.0, max(0.0, (p - 0.2) / 0.4))
                if line_progress > 0:
                    lw = int(600 * line_progress)
                    lx = (1080 - lw) // 2
                    draw.rectangle([lx, line_y, lx + lw, line_y + 3],
                                   fill=(*C_GOLD, int(255 * line_progress)))

                # Logo scale-in
                if has_logo:
                    logo_p = min(1.0, max(0.0, (p - 0.3) / 0.4))
                    if logo_p > 0:
                        try:
                            base = Image.open("avatar.png").convert("RGBA")
                            sw = int(logo_w * (0.6 + 0.4 * logo_p))
                            sh = int(logo_h * (0.6 + 0.4 * logo_p))
                            logo = base.resize((sw, sh),
                                               Image.Resampling.LANCZOS)
                            lx = (1080 - sw) // 2
                            ly = 720
                            img.paste(logo, (lx, ly), logo)
                        except Exception:
                            pass

                # Title fade-in
                title_p = min(1.0, max(0.0, (p - 0.5) / 0.4))
                if title_p > 0:
                    self._draw_text_centered(
                        draw, "HADITH OF THE DAY",
                        980, font_title,
                        (*C_GOLD, int(255 * title_p)))

                # Subtitle
                if title_p > 0.5:
                    self._draw_text_centered(
                        draw, "SAWAJ STUDIO Presents",
                        1080, font_sub,
                        (180, 160, 130, int(200 * title_p)))

                # Sparkles
                self._draw_sparkles(draw, t)

            # ==============================
            # MAIN (3-Language display)
            # ==============================
            elif t < self.intro + voice_dur:
                mt = t - self.intro
                alpha = min(1.0, mt / 0.5)

                # Top badge — Hadith number
                if hadith_label:
                    self._draw_badge(draw, hadith_label, y=180)

                # Watermark logo (top-right, semi-transparent)
                if has_logo:
                    try:
                        wm = Image.open("avatar.png").convert("RGBA").resize(
                            (160, 68), Image.Resampling.LANCZOS)
                        wm_alpha = wm.copy()
                        # Reduce alpha
                        alpha_layer = wm_alpha.split()[3].point(
                            lambda a: int(a * 0.55))
                        wm_alpha.putalpha(alpha_layer)
                        img.paste(wm_alpha, (1080 - 180, 180), wm_alpha)
                    except Exception:
                        pass

                # Floating logo (main animated)
                if has_logo:
                    try:
                        logo = Image.open("avatar.png").convert("RGBA").resize(
                            (logo_w, logo_h), Image.Resampling.LANCZOS)
                        # Sine wave motion
                        x = 80 + int(30 * math.sin(mt * 0.8))
                        y = 1500 + int(20 * math.sin(mt * 1.2))
                        img.paste(logo, (x, y), logo)
                    except Exception:
                        pass

                # ---- Language block (3 languages stacked) ----
                block_y = 780
                line_gap = 130

                # Hindi
                if hindi:
                    draw.ellipse([130, block_y + 22, 162, block_y + 54],
                                 fill=(*C_HINDI, int(255 * alpha)))
                    draw.text((190 + 3, block_y + 3), hindi,
                              fill=(0, 0, 0, int(220 * alpha)), font=font_hindi)
                    draw.text((190, block_y), hindi,
                              fill=(*C_HINDI, int(255 * alpha)), font=font_hindi)
                    block_y += line_gap

                # Arabic / Urdu
                if urdu:
                    draw.ellipse([130, block_y + 22, 162, block_y + 54],
                                 fill=(*C_URDU, int(255 * alpha)))
                    draw.text((190 + 3, block_y + 3), urdu,
                              fill=(0, 0, 0, int(220 * alpha)), font=font_arabic)
                    draw.text((190, block_y), urdu,
                              fill=(*C_URDU, int(255 * alpha)), font=font_arabic)
                    block_y += line_gap

                # English
                if english:
                    draw.ellipse([130, block_y + 22, 162, block_y + 54],
                                 fill=(*C_ENGLISH, int(255 * alpha)))
                    draw.text((190 + 3, block_y + 3), english,
                              fill=(0, 0, 0, int(220 * alpha)), font=font_lang)
                    draw.text((190, block_y), english,
                              fill=(*C_ENGLISH, int(255 * alpha)), font=font_lang)

                # Progress bar
                self._draw_progress(draw, mt, voice_dur)

                # Sparkles
                self._draw_sparkles(draw, t)

            # ==============================
            # OUTRO (JazakAllah + CTA)
            # ==============================
            else:
                ot = t - (self.intro + voice_dur)
                alpha = min(1.0, ot / 0.5)

                # JazakAllah
                self._draw_text_centered(
                    draw, "JazakAllah Khair",
                    780, font_outro,
                    (*C_GOLD, int(255 * alpha)))

                # CTA icons row
                if alpha > 0.4:
                    cta_y = 960
                    cta_items = [
                        ("👍 LIKE", 200),
                        ("🔔 SUBSCRIBE", 460),
                        ("💬 SHARE", 760),
                    ]
                    for label, x in cta_items:
                        try:
                            fnt = self._load_font(36, "latin", bold=True)
                            bbox = draw.textbbox((0, 0), label, font=fnt)
                            w = bbox[2] - bbox[0]
                            draw.text((x, cta_y), label,
                                      fill=(255, 240, 200, int(255 * alpha)),
                                      font=fnt)
                        except Exception:
                            pass

                # Follow text
                if alpha > 0.6:
                    self._draw_text_centered(
                        draw, "Follow @sawajstudio",
                        1120, font_cta,
                        (220, 190, 130, int(255 * alpha)))

                # Logo center-bottom
                if has_logo:
                    try:
                        logo = Image.open("avatar.png").convert("RGBA").resize(
                            (260, 110), Image.Resampling.LANCZOS)
                        img.paste(logo, ((1080 - 260) // 2, 1260), logo)
                    except Exception:
                        pass

                # Sparkles
                self._draw_sparkles(draw, t)

            img.save(f"{out_dir}/frame_{fi:05d}.png")

        log_step("frames.py", "Frames done", "ok",
                 f"{frames_count} files in {out_dir}")
        return total
