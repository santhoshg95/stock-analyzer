"""Regression coverage for the explainable news-analysis integration."""

import unittest
from unittest.mock import Mock, patch

from src.news.analysis_service import NewsAnalysisService


RSS = b"""<rss><channel>
<item><title>SBIN profit growth beats estimates</title><description>Strong expansion</description><source>Example</source><pubDate>Mon, 20 Jul 2026 10:00:00 GMT</pubDate></item>
<item><title>SBIN wins large contract</title><description>Record order</description><source>Example</source><pubDate>Mon, 20 Jul 2026 09:00:00 GMT</pubDate></item>
</channel></rss>"""


class NewsAnalysisServiceTests(unittest.TestCase):
    @patch("src.news.analysis_service.requests.get")
    def test_bullish_headlines_produce_explainable_score(self, get):
        response = Mock(content=RSS)
        response.raise_for_status.return_value = None
        get.return_value = response

        result = NewsAnalysisService.analyze("SBIN")

        self.assertTrue(result["available"])
        self.assertEqual(result["sentiment"], "BULLISH")
        self.assertGreater(result["score"], 0)
        self.assertEqual(result["article_count"], 2)
        self.assertEqual(len(result["headlines"]), 2)
