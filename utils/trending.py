# utils/trending.py

from pytrends.request import TrendReq
from config import Config
from newsapi import NewsApiClient
import feedparser

def fetch_google_trends(region='india', n=10):
    pytrends = TrendReq(hl='en-US', tz=330)
    trends_df = pytrends.trending_searches(pn='IN')
    print(trends_df)
    return trends_df[0].tolist()[:n]

def fetch_google_news_rss(n=10, query="India"):
    try:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)
        headlines = [entry.title for entry in feed.entries[:n]]
        return headlines
    except Exception as e:
        print(f"[Google News RSS Error] {e}")
        return []

def fetch_news_headlines(n=10):
    return fetch_google_news_rss(n=n, query="India")

