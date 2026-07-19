"""
Rule Engine Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.context.context_builder import ContextBuilder
from src.rules.rule_engine import RuleEngine


def main():

    builder = ContextBuilder()
    context = builder.build("SBIN")

    engine = RuleEngine()

    report = engine.evaluate(context)

    print("=" * 100)
    print("RULE ENGINE")
    print("=" * 100)

    print(f"Overall Status : {'PASS' if report['passed'] else 'FAIL'}")
    print()

    for rule in report["results"]:

        status = "PASS" if rule.passed else "FAIL"

        print(f"{rule.name:15} {status:5} {rule.severity:8} {rule.reason}")

    print("=" * 100)


if __name__ == "__main__":
    main()