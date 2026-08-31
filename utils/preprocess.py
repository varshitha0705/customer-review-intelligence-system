import gzip
import json
import re
import pandas as pd


def load_amazon_reviews(file_path, limit=10000):

    reviews = []

    with gzip.open(file_path, "rt", encoding="utf-8") as file:

        for i, line in enumerate(file):

            if i >= limit:
                break

            review = json.loads(line)

            reviews.append({
                "Rating": review.get("overall"),
                "Review": review.get("reviewText"),
                "Summary": review.get("summary"),
                "Verified": review.get("verified"),
                "Date": review.get("reviewTime"),
                "Product_ID": review.get("asin")
            })

    return pd.DataFrame(reviews)


def clean_review(text):

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text
