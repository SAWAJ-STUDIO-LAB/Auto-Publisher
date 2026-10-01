"""Logo/avatar maker with premium border + glow."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from logger import log_file_start, log_file_end, log_step


class Logo:
    def __init__(self):
        log_file_start("logo.py", "Logo/avatar generation")
        log_file_end("logo.py", "success", "Ready")

    def make(self, outfile="avatar.png"):
        log_step("logo.py", "make() starting", "ok")

        # Try user logo files first
        for src in ["logo.png", "logo.jpg", "assets/logo.png", "assets/logo.jpg"]:
            if os.path.exists(src):
                try:
                    log_step("logo.py", f"Found {src}", "ok")
                    img = Image.open(src).convert("RGBA")

                    # Resize if too big
                    if img.width > 400:
                        ratio = 400 / img.width
                        img = img.resize(
                            (400, int(img.height * ratio)),
                            Image.Resampling.LANCZOS)

                    border, bottom = 12, 26
                    nw = img.width + border * 2
                    nh = img.height + border + bottom
                    canvas = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
                    draw = ImageDraw.Draw(canvas)

                    # Gold border
                    draw.rectangle([0, 0, nw - 1, nh - 1],
                                   outline=(212, 175, 55, 255), width=border)

                    # Inner thin gold line
                    draw.rectangle([border, border,
                                    nw - border - 1, nh - bottom - 1],
                                   outline=(255, 215, 100, 200), width=2)

                    # Bottom strip
                    draw.rectangle([0, nh - bottom, nw - 1, nh - 1],
                                   fill=(20, 15, 8, 245))

                    # Paste logo
                    canvas.paste(img, (border, border), img)

                    # Glow
                    glow = canvas.filter(ImageFilter.GaussianBlur(6))
                    final = Image.alpha_composite(glow, canvas)
                    final.save(outfile)
                    log_step("logo.py", f"Saved {outfile} from {src}", "ok",
                             f"{final.width}x{final.height}")
                    return True
                except Exception as e:
                    log_step("logo.py", f"Err with {src}", "fail", str(e)[:60])

        # Default fallback avatar
        try:
            log_step("logo.py", "Generating default avatar", "info")
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
            log_step("logo.py", "Default avatar saved", "ok")
            return True
        except Exception as e:
            log_step("logo.py", "Default avatar failed", "fail", str(e)[:60])
            return False
