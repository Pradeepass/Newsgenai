# from pymongo import MongoClient

# # 🔹 Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["newsgenai"]
# collection = db["news_articles"]

# def save_to_db(article):
#     """Saves a news article to MongoDB."""
#     try:
#         collection.insert_one(article)
#         print(f"✅ Saved: {article['title']}")
#     except Exception as e:
#         print(f"🚨 Error saving article: {article['title']} → {e}")

# def fetch_unprocessed_articles():
#     """Fetch articles that have not been processed yet."""
#     articles = list(collection.find({"processed": False}, {"_id": 0}))
#     return articles

# def update_cleaned_article(article):
#     """Update a processed article in MongoDB."""
#     result = collection.update_one({"url": article["url"]}, {"$set": article})
#     if result.matched_count > 0:
#         print(f"✅ Updated: {article['title']} (Processed ✅)")

# def fetch_training_data():
#     """Fetch labeled training data for model training."""
#     articles = list(collection.find({"category": {"$exists": True}}, {"content": 1, "category": 1, "_id": 0}))
#     return articles

# def fetch_uncategorized_articles():
#     """Fetch preprocessed articles that have not been categorized yet."""
#     articles = list(collection.find({"processed": True, "category": {"$exists": False}}, {"_id": 0}))
#     return articles

# def update_categorized_article(article):
#     """Update an article with its assigned category."""
#     result = collection.update_one({"url": article["url"]}, {"$set": article})
#     if result.matched_count > 0:
#         print(f"✅ Categorized: {article['title']} → {article['category']}")

# def fetch_available_categories():
#     """Fetch unique categories stored in MongoDB."""
#     categories = collection.distinct("category")
#     return [cat for cat in categories if cat]  # Remove empty categoriesfrom pymongo import MongoClient

# # 🔹 Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["newsgenai"]
# collection = db["news_articles"]

# def save_to_db(article):
#     """Saves a news article to MongoDB."""
#     try:
#         collection.insert_one(article)
#         print(f"✅ Saved: {article['title']}")
#     except Exception as e:
#         print(f"🚨 Error saving article: {article['title']} → {e}")

# def fetch_unprocessed_articles():
#     """Fetch articles that have not been processed yet."""
#     articles = list(collection.find({"processed": False}, {"_id": 0}))
#     return articles

# def update_cleaned_article(article):
#     """Update a processed article in MongoDB."""
#     result = collection.update_one({"url": article["url"]}, {"$set": article})
#     if result.matched_count > 0:
#         print(f"✅ Updated: {article['title']} (Processed ✅)")

# def fetch_training_data():
#     """Fetch labeled training data for model training."""
#     articles = list(collection.find({"category": {"$exists": True}}, {"content": 1, "category": 1, "_id": 0}))
#     return articles

# def fetch_uncategorized_articles():
#     """Fetch preprocessed articles that have not been categorized yet."""
#     articles = list(collection.find({"processed": True, "category": {"$exists": False}}, {"_id": 0}))
#     return articles

# def update_categorized_article(article):
#     """Update an article with its assigned category."""
#     result = collection.update_one({"url": article["url"]}, {"$set": article})
#     if result.matched_count > 0:
#         print(f"✅ Categorized: {article['title']} → {article['category']}")

# def fetch_available_categories():
#     """Fetch unique categories stored in MongoDB."""
#     categories = collection.distinct("category")
#     return [cat for cat in categories if cat]  # Remove empty categories


from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["newsgenai"]
collection = db["news_articles"]

def save_to_db(article):
    try:
        collection.insert_one(article)
        print(f"✅ Saved: {article['title']}")
    except Exception as e:
        print(f"❌ Error saving article → {e}")

def fetch_unprocessed_articles():
    return list(collection.find({"processed": False}, {"_id": 0}))

def update_cleaned_article(article):
    collection.update_one({"url": article["url"]}, {"$set": article})

def fetch_training_data():
    return list(collection.find({"processed": True, "category": {"$exists": True}}, {"content": 1, "category": 1, "_id": 0}))

def fetch_uncategorized_articles():
    return list(collection.find({"processed": True, "category": {"$exists": False}}, {"_id": 0}))

def update_categorized_article(article):
    collection.update_one({"url": article["url"]}, {"$set": article})

def fetch_available_categories():
    return collection.distinct("category")