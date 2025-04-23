import os
import sys

# 🔹 Ensure all module paths are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "module_1_collection")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "module_2_preprocessing")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "module_3_categorization")))

from module_1_collection.news_api import fetch_news # Module 1: Fetch News
from module_2_preprocessing.preprocess import preprocess_articles  # Module 2: Preprocess News
from module_3_categorization.categorize import categorize_articles  # Module 3: Categorize News 

def main():
    print("\n📰 *Step 1: Fetching News from API...*")
    fetch_news()  # Fetches news and stores in MongoDB

    print("\n🔍 *Step 2: Preprocessing Fetched News...*")
    preprocess_articles()  # Cleans text and updates MongoDB

    print("\n🎓 *Step 3: Training Model with Real-Time MongoDB Data...*")
    os.system("python module_3_categorization/train_model.py")  # ✅ Train the ML Model

    print("\n📊 *Step 4: Categorizing Preprocessed News...*")
    categorize_articles()  # Categorizes news and updates MongoDB

    print("\n✅ *Full Pipeline Execution Completed Successfully!*")
 
if __name__ == "__main__":
    main()
