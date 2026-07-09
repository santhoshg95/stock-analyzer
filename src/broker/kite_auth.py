"""
Kite Authentication

Creates and returns an authenticated KiteConnect client.
"""

import os

from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()


class KiteAuthentication:

    def __init__(self):

        api_key = os.getenv("KITE_API_KEY")
        access_token = os.getenv("KITE_ACCESS_TOKEN")

        if not api_key:
            raise ValueError("KITE_API_KEY not found in .env")

        if not access_token:
            raise ValueError("KITE_ACCESS_TOKEN not found in .env")

        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)

    # -------------------------------------------------

    def get_client(self):
        """
        Returns authenticated KiteConnect client.
        """
        return self.kite

    # -------------------------------------------------

    def profile(self):
        """
        Returns logged-in user profile.
        """
        return self.kite.profile()