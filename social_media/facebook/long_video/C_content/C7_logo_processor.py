# ============================================================
# FILE:      C7_logo_processor.py
# PATH:      social_media/facebook/story_video/C_content/C7_logo_processor.py
# PURPOSE:   Process logo → avatar with border + glow
# ============================================================

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from A_core.A2_logger import log_file_start, log_file_end, log_step


class LogoProcessor:

    def __init__(self):
        log_file_start("C7_logo_processor.py", "Logo processing")
        log_file_end("C7_logo_processor.py", "success", "Ready")

    def make(self, outfile="avatar.png"):
        log_step("C7_logo_processor.py", "make() starting", "ok")

        for src in ["logo.png", "logo.jpg", "assets/logo.png", "assets/logo.jpg"]:
            if os.path.exists(src):
                try:
                    log_step("C7_logo_processor.py", f"Found {src}", "ok")
                    img = Image.open(src).convert("RGBA")
                    if img.width > 400:
                        ratio = 400 / img.width
                        img = img.resize((400, int(img.height * ratio)),
                                         Image.Resampling.LANCZOS)

                    border, bottom = 12, 26
                    nw = img.width + border * 2
                    nh = img.height + border + bottom
                    canvas = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
                    draw = ImageDraw.Draw(canvas)

                    draw.rectangle([0, 0, nw - 1, nh - 1],
                                   outline=(212, 175, 55, 255), width=border)
                    draw.rectangle([border, border, nw - border - 1,
                                    nh - bottom - 1],
                                   outline=(255, 215, 100, 200), width=2)
                    draw.rectangle([0, nh - bottom, nw - 1, nh - 1],
                                   fill=(20, 15, 8, 245))
                    canvas.paste(img, (border, border), img)
                    glow = canvas.filter(ImageFilter.GaussianBlur(6))
                    final = Image.alpha_composite(glow, canvas)
                    final.save(outfile)
                    log_step("C7_logo_processor.py", f"Saved {outfile}", "ok")
                    return True
                except Exception as e:
                    log_step("C7_logo_processor.py", f"Err {src}", "fail", str(e)[:60])

        try:
            log_step("C7_logo_processor.py", "Default avatar", "info")
            canvas = Image.new("RGBA", (400, 170), (0, 0, 0, 0))
            draw = ImageDraw.Draw(canvas)
            draw.rounded_rectangle([6, 6, 394, 164], radius=16,
                                   fill=(16, 12, 6, 245),
                                   outline=(212, 175, 55, 255), width=5)
            try:
                fnt = ImageFont.truetype(
                    os.path.expanduser("~/.fonts/NotoSans-Bold.ttf"), 44)
            except Exception:
                fnt = ImageFont.load_default()
            draw.text((200, 65), "SAWAJ",
                      fill=(230, 200, 130, 255), font=fnt, anchor="mm")
            draw.text((200, 115), "STUDIO",
                      fill=(200, 170, 110, 255), font=fnt, anchor="mm")
            canvas.save(outfile)
            log_step("C7_logo_processor.py", "Default avatar saved", "ok")
            return True
        except Exception as e:
            log_step("C7_logo_processor.py", "Default failed", "fail", str(e)[:60])
            return False
