"""
News Collection Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.news.service.news_service import NewsService


def main():

    service = NewsService()

    articles = service.get_news("SBIN")

    print("=" * 100)
    print("NEWS COLLECTION")
    print("=" * 100)

    print(f"Articles Found : {len(articles)}")

    print()

    for article in articles[:5]:

        print("-" * 100)

        print(article.title)

        print()

        print(article.source)

        print()

        print(article.link)

    print("=" * 100)


if __name__ == "__main__":

    main()