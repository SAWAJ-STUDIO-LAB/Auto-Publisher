"""
Hadith fetcher — random from Bukhari/Muslim/AbuDawud/Tirmidhi.
"""
import os
import random
from shared.session import session
from shared.telegram import api_status, send_tg
from shared.utils import sanitize
from shared.logger import get_logger

logger = get_logger("hadith")

BOOKS = [
    {"eng": "eng-bukhari", "ara": "ara-bukhari", "name":
