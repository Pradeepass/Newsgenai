import re
import nltk
from textblob import Word
from nltk.corpus import stopwords
from database import fetch_unprocessed_articles, update_cleaned_article

# 🔹 Automatically download required NLTK datasets
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

# Load NLTK stopwords
STOPWORDS = set(stopwords.words("english"))

def clean_text(text):
    """Removes HTML tags, special characters, and stopwords."""
    if not text:
        return ""

    text = re.sub(r"<.*?>", "", text)  # Remove HTML tags
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    text = text.lower().strip()  # Convert to lowercase
    words = [word for word in text.split() if word not in STOPWORDS]  # Remove stopwords
    return " ".join(words)

def lemmatize_text(text):
    """Lemmatizes text using TextBlob."""
    return " ".join([Word(word).lemmatize() for word in text.split()])

def preprocess_articles():
    """Fetch, clean, and update news articles in MongoDB."""
    articles = fetch_unprocessed_articles()

    if not articles:
        print("🚨 No unprocessed articles found in MongoDB.")
        return

    print(f"🔄 Found {len(articles)} unprocessed articles.")
    print(f"🔄 Processing {len(articles)} articles...")

    for article in articles:
        if "url" not in article:
            print(f"⚠️ Skipping: '{article.get('title', 'Unknown Title')}' (Missing URL ❌)")
            continue  # Skip processing if URL is missing

        print(f"⚡ Processing: {article['title']}")  

        article["content"] = clean_text(article.get("content", ""))
        article["title"] = clean_text(article.get("title", ""))
        article["content"] = lemmatize_text(article["content"])
        article["processed"] = True  

        update_cleaned_article(article)  # Update MongoDB

        print(f"✅ Updated: {article['title']} (Processed ✅)")

    print("🎯 Preprocessing completed successfully!")
