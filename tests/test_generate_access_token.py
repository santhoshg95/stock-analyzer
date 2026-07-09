"""
Generate Zerodha Access Token
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from kiteconnect import KiteConnect
from src.config.secrets import Secrets


def main():

    kite = KiteConnect(api_key=Secrets.KITE_API_KEY)

    request_token = input("Enter Request Token: ").strip()

    data = kite.generate_session(
        request_token=request_token,
        api_secret=Secrets.KITE_API_SECRET,
    )

    print("\n" + "=" * 80)
    print("SESSION GENERATED")
    print("=" * 80)

    print("Access Token:")
    print(data["access_token"])

    print("=" * 80)


if __name__ == "__main__":
    main()