"""
Logo/avatar generator — uses repo logo.png if present,
otherwise builds a "SAWAJ STUDIO" placeholder.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from shared.logger import get_logger

logger = get_logger("logo")

CANDIDATE_PATHS = ["logo.png", "logo.jpg", "assets/logo.png", "assets/logo.jpg"]


def make_logo() -> bool:
    """Create avatar.png. Returns True if successful."""
    # Try repo logo
    for src in CANDIDATE_PATHS:
        if os.path.exists(src):
            try:
                img = Image.open(src).convert("RGBA")
                border, bottom = 10, 22
                nw, nh = img.width + border * 2, img.height + border + bottom
                canvas = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
                draw = ImageDraw.Draw(canvas)
                draw.rectangle([0, 0, nw - 1, nh - 1], outline=(212, 175, 55, 255), width=border)
                draw.rectangle([0, nh - bottom, nw - 1, nh - 1], fill=(20, 15, 8, 240))
                canvas.paste(img, (border, border), img)
                glow = canvas.filter(ImageFilter.GaussianBlur(4))
                Image.alpha_composite(glow, canvas).save("avatar.png")
                return True
            except Exception as e:
                logger.warning(f"Logo build failed for {src}: {e}")

    # Placeholder
    try:
        canvas = Image.new("RGBA", (400, 170), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle(
            [6, 6, 394, 164], radius=16,
            fill=(16, 12, 6, 245), outline=(212, 175, 55, 255), width=5,
        )
        try:
            fnt = ImageFont.truetype(os.path.expanduser("~/.fonts/NotoSans-Bold.ttf"), 44)
        except Exception:
            fnt = ImageFont.load_default()
        draw.text((200, 65), "SAWAJ", fill=(230, 200, 130, 255), font=fnt, anchor="mm")
        draw.text((200, 115), "STUDIO", fill=(200, 170, 110, 255), font=fnt, anchor="mm")
        canvas.save("avatar.png")
        return True
    except Exception as e:
        logger.error(f"Placeholder logo failed: {e}")
        return False
