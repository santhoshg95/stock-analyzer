"""
Application Secrets
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Secrets:

    KITE_API_KEY = os.getenv("KITE_API_KEY")

    KITE_API_SECRET = os.getenv("KITE_API_SECRET")

    KITE_ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")

    BROKER = os.getenv("BROKER", "paper")

    CAPITAL = float(os.getenv("CAPITAL", 1000000))

    RISK_PERCENT = float(os.getenv("RISK_PERCENT", 1))