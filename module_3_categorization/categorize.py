import os
import joblib
import re
import nltk
from database import fetch_uncategorized_articles, update_categorized_article, fetch_available_categories

nltk.download("stopwords")
nltk.download("punkt")

STOPWORDS = set(nltk.corpus.stopwords.words("english"))

# 🔹 Load trained model & vectorizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "news_classifier.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "model", "tfidf_vectorizer.pkl")

if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError("🚨 Model or Vectorizer file not found. Run 'train_model.py' first.")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def clean_text(text):
    """Preprocess text for classification."""
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower().strip()
    words = [word for word in text.split() if word not in STOPWORDS]
    return " ".join(words)

def categorize_articles():
    """Fetches preprocessed articles, classifies them dynamically, and updates MongoDB."""
    articles = fetch_uncategorized_articles()
    available_categories = fetch_available_categories()  # ✅ Dynamically get categories

    if not articles:
        print("🚨 No uncategorized articles found!")
        return

    print(f"🔄 Categorizing {len(articles)} articles dynamically...")

    for article in articles:
        cleaned_text = clean_text(article.get("content", ""))
        X_input = vectorizer.transform([cleaned_text])  # Transform text using TF-IDF
        predicted_category = model.predict(X_input)[0]

        if predicted_category in available_categories:
            article["category"] = predicted_category  # Assign category dynamically
        else:
            article["category"] = "Uncategorized"  # Default if no match

        update_categorized_article(article)
        print(f"✅ Categorized: {article['title']} → {article['category']}")

    print("🎯 Categorization completed successfully!")