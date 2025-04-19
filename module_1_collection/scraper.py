import requests
from bs4 import BeautifulSoup
from db import save_to_db

def scrape_news(url):
    """ Scrapes news articles from a website """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for article in soup.find_all("article"):
        title = article.find("h2").text if article.find("h2") else "No Title"
        link = article.find("a")["href"] if article.find("a") else "#"

        news_item = {
            "title": title,
            "url": link,
            "source": url,
            "content": "",
            "published_at": "",
        }
        save_to_db(news_item)

# Example usage:
# scrape_news("https://example-news-site.com")