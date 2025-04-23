import sys
sys.path.append('C:/Users/HP/OneDrive/Documents/newsgenai')
import os
import re
import joblib
import nltk
from database import fetch_training_data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Download necessary NLTK resources
nltk.download("stopwords")
nltk.download("punkt")

STOPWORDS = set(nltk.corpus.stopwords.words("english"))

# Define paths to save the model and vectorizer
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "news_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")

# Create model directory if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)

def clean_text(text):
    """Preprocess text: remove special characters, lowercase, stopwords."""
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower().strip()
    words = [word for word in text.split() if word not in STOPWORDS]
    return " ".join(words)

def train_model():
    """Fetch training data, train model, and save it."""
    print("📥 Fetching training data from MongoDB...")
    training_data = fetch_training_data()

    if not training_data:
        print("🚫 No labeled training data found in MongoDB!")
        return

    print(f"📚 Found {len(training_data)} training samples.")

    texts = []
    labels = []

    for article in training_data:
        if "content" in article and "category" in article:
            cleaned = clean_text(article["content"])
            if cleaned:
                texts.append(cleaned)
                labels.append(article["category"])

    if not texts:
        print("🚫 No clean data available for training!")
        return

    print("🧠 Training model with TF-IDF + Naive Bayes...")
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(texts)

    model = MultinomialNB()
    model.fit(X_train, labels)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(f"✅ Model saved to: {MODEL_PATH}")
    print(f"✅ Vectorizer saved to: {VECTORIZER_PATH}")
    print("🎯 Model training completed successfully!")

if __name__ == "_main_":
    train_model()