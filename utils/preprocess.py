import gzip
import json
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