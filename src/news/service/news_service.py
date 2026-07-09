"""
News Service
"""

from src.news.collectors.google_news import GoogleNewsCollector


class NewsService:

    def __init__(self):

        self.collector = GoogleNewsCollector()

    def get_news(self, symbol):

        return self.collector.fetch(symbol)