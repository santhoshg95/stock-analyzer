"""
Secrets Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.config.secrets import Secrets


print("=" * 80)

print("CONFIGURATION")

print("=" * 80)

print("Broker :", Secrets.BROKER)

print("Capital :", Secrets.CAPITAL)

print("Risk :", Secrets.RISK_PERCENT)

print("=" * 80)