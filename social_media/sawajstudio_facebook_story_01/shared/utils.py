"""
Generic helpers: sanitize text, run shell commands, download files.
"""
import os
import re
import subprocess
from shared.session import session
from shared.logger import get_logger

logger = get_logger("utils")


def sanitize(text) -> str:
    """Remove invisible unicode chars, quotes, newlines."""
    if not text:
        return ""
    t = re.sub(r"[\u200b-\u200f\ufeff\u202a-\u202e]", "", str(text))
    return t.replace('"', "").replace("'", "").replace("\n", " ").strip()


def strip_code_fence(text: str) -> str:
    """Remove ```...``` wrappers from AI output."""
    if not text:
        return ""
    return re.sub(r"^```.*?```", "", text, flags=re.DOTALL).strip()


def run_cmd(cmd: str) -> None:
    """Run shell command, raise on failure."""
    logger.info(f"[CMD] {cmd[:140]}...")
    subprocess.run(cmd, shell=True, check=True)


def download(url: str, path: str, min_size: int = 12000) -> bool:
    """Download URL to path if size >= min_size."""
    try:
        r = session.get(url, timeout=35)
        if r.status_code == 200 and len(r.content) >= min_size:
            with open(path, "wb") as f:
                f.write(r.content)
            return True
    except Exception as e:
        logger.warning(f"Download failed: {e}")
    return False


def ensure_dirs(*paths: str) -> None:
    """Create directories if missing."""
    for p in paths:
        os.makedirs(p, exist_ok=True)
