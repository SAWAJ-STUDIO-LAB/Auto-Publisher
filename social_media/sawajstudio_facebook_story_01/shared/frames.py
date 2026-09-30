"""
Frame generator for Story video:
- Intro (1.5s) with "SAWAJ STUDIO / Morning Story"
- Body with floating logo
- Outro (1.7s) with "JazakAllah Khair"
"""
import os
from PIL import Image, ImageDraw, ImageFont
from shared.logger import get_logger

logger = get_logger("frames")

FPS = 25
INTRO = 1.5
OUTRO = 1.7


def _load_fonts():
    try:
        big = ImageFont.truetype(os.path.expanduser("~/.fonts/NotoSans-Bold.ttf"), 68)
        small = ImageFont.truetype(os.path.expanduser("~/.fonts/NotoSans-Bold.ttf"), 42)
    except Exception:
        big = small = ImageFont.load_default()
    return big, small


def build_story_frames(
    voice_dur: float,
    has_logo: bool,
    outdir: str = "s_frames",
) -> tuple:
    """Generate all PNG frames. Returns (outdir, total_duration)."""
    os.makedirs(outdir, exist_ok=True)
    font_big, font_s = _load_fonts()

    total = INTRO + voice_dur + OUTRO
    logo_w, logo_h = 220, 95
    max_x, max_y = 1080 - logo_w, 1920 - logo_h

    for fi in range(int(total * FPS)):
        t = fi / FPS
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if t < INTRO:
            a = min(1.0, t / 0.5)
            draw.text((540, 870), "SAWAJ STUDIO",
                      fill=(220, 190, 120, int(255 * a)), font=font_big, anchor="mm")
            draw.text((540, 960), "Morning Story",
                      fill=(180, 160, 130, int(200 * a)), font=font_s, anchor="mm")

        elif t < INTRO + voice_dur:
            mt = t - INTRO
            if has_logo:
                try:
                    logo = Image.open("avatar.png").convert("RGBA").resize(
                        (logo_w, logo_h), Image.Resampling.LANCZOS
                    )
                    x = abs((int(mt * 200) + 60) % (2 * max_x) - max_x)
                    y = abs((int(mt * 150) + 120) % (2 * max_y) - max_y)
                    img.paste(logo, (x, y), logo)
                except Exception:
                    pass

        else:
            ot = t - (INTRO + voice_dur)
            a = min(1.0, ot / 0.55)
            draw.text((540, 860), "JazakAllah Khair",
                      fill=(220, 190, 120, int(255 * a)), font=font_big, anchor="mm")
            if has_logo:
                try:
                    logo = Image.open("avatar.png").convert("RGBA").resize(
                        (190, 80), Image.Resampling.LANCZOS
                    )
                    img.paste(logo, (445, 970), logo)
                except Exception:
                    pass

        img.save(f"{outdir}/frame_{fi:05d}.png")

    logger.info(f"Frames generated → {outdir} ({int(total * FPS)} frames)")
    return outdir, total
