from pathlib import Path
import json
import numpy as np
import pandas as pd

# --------------------------------------------------
# Configuration
# --------------------------------------------------

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "books_ratings_5core.csv"
)

MODEL_OUTPUT = (
    PROJECT_ROOT
    / "models"
    / "popularity_baseline.csv"
)

METRICS_OUTPUT = (
    PROJECT_ROOT
    / "artifacts"
    / "reports"
    / "popularity_baseline_metrics.json"
)

MIN_REVIEWS = 50

# --------------------------------------------------
# Create Output Directories
# --------------------------------------------------

Path(
    PROJECT_ROOT
    / "models"
).mkdir(exist_ok=True)

Path(
    PROJECT_ROOT
    / "artifacts"
    / "reports"
).mkdir(
    parents=True,
    exist_ok=True
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(
    INPUT_FILE,
    usecols=[
        "Title",
        "review/score"
    ]
)

print(f"Loaded {len(df):,} reviews")

# --------------------------------------------------
# Aggregate Book Statistics
# --------------------------------------------------

print("Calculating book statistics...")

book_stats = (
    df.groupby("Title")
    .agg(
        avg_rating=("review/score", "mean"),
        review_count=("review/score", "count")
    )
    .reset_index()
)

# --------------------------------------------------
# Apply Minimum Review Threshold
# --------------------------------------------------

book_stats = book_stats[
    book_stats["review_count"] >= MIN_REVIEWS
]

print(
    f"Eligible books: "
    f"{len(book_stats):,}"
)

# --------------------------------------------------
# Weighted Popularity Score
# --------------------------------------------------

book_stats["weighted_score"] = (
    book_stats["avg_rating"]
    * np.log10(book_stats["review_count"])
)

# --------------------------------------------------
# Ranking
# --------------------------------------------------

book_stats = book_stats.sort_values(
    by="weighted_score",
    ascending=False
)

book_stats["rank"] = (
    range(
        1,
        len(book_stats) + 1
    )
)

# Reorder columns

book_stats = book_stats[
    [
        "rank",
        "Title",
        "avg_rating",
        "review_count",
        "weighted_score"
    ]
]

# --------------------------------------------------
# Save Model Artifact
# --------------------------------------------------

book_stats.to_csv(
    MODEL_OUTPUT,
    index=False
)

print(
    f"Model saved to: "
    f"{MODEL_OUTPUT}"
)

# --------------------------------------------------
# Generate Metrics Report
# --------------------------------------------------

metrics = {
    "dataset_reviews": int(len(df)),
    "dataset_books": int(df["Title"].nunique()),
    "minimum_reviews": int(MIN_REVIEWS),
    "eligible_books": int(len(book_stats)),
    "average_rating": float(
        round(
            book_stats["avg_rating"].mean(),
            4
        )
    ),
    "top_book": str(
        book_stats.iloc[0]["Title"]
    ),
    "top_book_rating": float(
        round(
            book_stats.iloc[0]["avg_rating"],
            4
        )
    )
}

with open(
    METRICS_OUTPUT,
    "w"
) as f:
    json.dump(
        metrics,
        f,
        indent=4
    )

print(
    f"Metrics saved to: "
    f"{METRICS_OUTPUT}"
)

# --------------------------------------------------
# Preview Top 20
# --------------------------------------------------

print("\nTop 20 Books")
print("-" * 80)

print(
    book_stats.head(20).to_string(
        index=False
    )
)
