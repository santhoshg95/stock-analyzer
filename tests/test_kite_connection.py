"""
Test Zerodha Kite Connection
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

    kite.set_access_token(Secrets.KITE_ACCESS_TOKEN)

    profile = kite.profile()

    print("=" * 80)
    print("ZERODHA CONNECTION")
    print("=" * 80)

    print(f"User ID      : {profile['user_id']}")
    print(f"User Name    : {profile['user_name']}")
    print(f"Email        : {profile['email']}")
    print(f"Broker       : {profile['broker']}")
    print(f"User Type    : {profile['user_type']}")

    print("=" * 80)


if __name__ == "__main__":
    main()