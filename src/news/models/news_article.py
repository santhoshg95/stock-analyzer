"""
News Article Model
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsArticle:

    title: str

    summary: str

    source: str

    published: datetime

    link: str