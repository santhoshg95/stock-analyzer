"""
Authentication Service
"""

import webbrowser

from src.broker.kite_auth import KiteAuthentication


class AuthenticationService:

    @staticmethod
    def login():

        auth = KiteAuthentication()

        url = auth.login_url()

        print("=" * 80)
        print("Open the following URL")
        print("=" * 80)

        print(url)

        print("=" * 80)

        webbrowser.open(url)