"""
Kite Login Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.services.auth_service import AuthenticationService


def main():

    AuthenticationService.login()


if __name__ == "__main__":

    main()