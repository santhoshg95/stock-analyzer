"""
Google News RSS Collector
"""

import feedparser

from src.news.models.news_article import NewsArticle


class GoogleNewsCollector:

    BASE_URL = (
        "https://news.google.com/rss/search?q={query}+stock"
    )

    def fetch(self, query: str):

        url = self.BASE_URL.format(query=query)

        feed = feedparser.parse(url)

        articles = []

        for entry in feed.entries:

            articles.append(

                NewsArticle(

                    title=entry.title,

                    summary=getattr(entry, "summary", ""),

                    source=getattr(entry, "source", {}).get(
                        "title",
                        "Google News"
                    ),

                    published=entry.published,

                    link=entry.link

                )

            )

        return articles