import json
import os
from config import ARTICLES_DIR

def save_article_json(article: dict) -> None:
    folder = os.path.join(ARTICLES_DIR, article["topic"])
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{article['id']}.json")
    with open(file_path, "w") as f:
        json.dump(article, f)
