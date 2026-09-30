import os, sys
from ..shared.telegram import send_tg
from ..shared.logger import get_logger

logger = get_logger("runner")

def main():
    logger.info("Executing Pipeline Module...")
    send_tg("🚀 Module Runner Triggered & Executed Successfully!")

if __name__ == "__main__":
    main()
