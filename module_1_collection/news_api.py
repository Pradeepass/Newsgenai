import requests
import sys
import os

# 🔹 Ensure correct import of database.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import save_to_db
from config import NEWS_API_KEY

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(country="us", category="technology"):
    """Fetches news articles from NewsAPI and saves them to MongoDB."""
    params = {"country": country, "category": category, "apiKey": NEWS_API_KEY}
    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()

    if data["status"] == "ok":
        for article in data["articles"]:
            news_item = {
                "title": article["title"],
                "url": article["url"],
                "content": article.get("content", ""),
                "source": article["source"]["name"],
                "published_at": article["publishedAt"],
                "processed": False  # Mark as unprocessed
            }
            save_to_db(news_item)
    else:
        print("🚨 Error fetching news!")