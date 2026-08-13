from pathlib import Path
import json
import numpy as np
import pandas as pd

# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "books_ratings_5core.csv"
)

MODEL_DIR = PROJECT_ROOT / "models"

REPORT_DIR = (
    PROJECT_ROOT
    / "artifacts"
    / "reports"
)

FULL_MODEL_OUTPUT = (
    MODEL_DIR
    / "popularity_baseline.csv"
)

TOP100_OUTPUT = (
    MODEL_DIR
    / "popularity_baseline_top100.csv"
)

METRICS_OUTPUT = (
    REPORT_DIR
    / "popularity_baseline_metrics.json"
)

MIN_REVIEWS = 50
TOP_N_PREVIEW = 20

# ============================================================
# Create Directories
# ============================================================

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Load Dataset
# ============================================================

print("Loading dataset...")

df = pd.read_csv(
    INPUT_FILE,
    usecols=[
        "Title",
        "review/score",
    ]
)

print(f"Loaded {len(df):,} reviews")

# ============================================================
# Calculate Book Statistics
# ============================================================

print("Calculating book statistics...")

book_stats = (
    df.groupby("Title")
      .agg(
          avg_rating=("review/score", "mean"),
          review_count=("review/score", "count"),
          positive_reviews=(
              "review/score",
              lambda x: (x >= 4).sum()
          )
      )
      .reset_index()
)

# ============================================================
# Apply Review Threshold
# ============================================================

book_stats = book_stats[
    book_stats["review_count"] >= MIN_REVIEWS
]

print(
    f"Eligible books: {len(book_stats):,}"
)

# ============================================================
# Additional Metrics
# ============================================================

total_reviews = len(df)

book_stats["positive_pct"] = (
    (
        book_stats["positive_reviews"]
        / book_stats["review_count"]
    ) * 100
)

book_stats["review_pct"] = (
    (
        book_stats["review_count"]
        / total_reviews
    ) * 100
)

# ============================================================
# Weighted Popularity Score
# ============================================================

book_stats["weighted_score"] = (
    book_stats["avg_rating"]
    * np.log10(book_stats["review_count"])
)

# ============================================================
# Rounding
# ============================================================

book_stats["avg_rating"] = (
    book_stats["avg_rating"]
    .round(3)
)

book_stats["positive_pct"] = (
    book_stats["positive_pct"]
    .round(2)
)

book_stats["review_pct"] = (
    book_stats["review_pct"]
    .round(4)
)

book_stats["weighted_score"] = (
    book_stats["weighted_score"]
    .round(3)
)

# ============================================================
# Ranking
# ============================================================

book_stats = book_stats.sort_values(
    by="weighted_score",
    ascending=False
)

book_stats["rank"] = range(
    1,
    len(book_stats) + 1
)

# ============================================================
# Reorder Columns
# ============================================================

book_stats = book_stats[
    [
        "rank",
        "Title",
        "avg_rating",
        "review_count",
        "positive_reviews",
        "positive_pct",
        "review_pct",
        "weighted_score"
    ]
]

# ============================================================
# Save Model Artifacts
# ============================================================

book_stats.to_csv(
    FULL_MODEL_OUTPUT,
    index=False
)

book_stats.head(100).to_csv(
    TOP100_OUTPUT,
    index=False
)

print(
    f"Model saved to:\n{FULL_MODEL_OUTPUT}"
)

print(
    f"Top 100 saved to:\n{TOP100_OUTPUT}"
)

# ============================================================
# Metrics Report
# ============================================================

positive_interactions = (
    df["review/score"] >= 4
).sum()

metrics = {
    "dataset_reviews": int(len(df)),
    "dataset_books": int(df["Title"].nunique()),
    "minimum_reviews": MIN_REVIEWS,
    "eligible_books": int(len(book_stats)),
    "positive_interaction_ratio_pct": round(
        (
            positive_interactions
            / len(df)
        ) * 100,
        2
    ),
    "average_eligible_book_rating": round(
        float(
            book_stats["avg_rating"].mean()
        ),
        3
    ),
    "top_book": str(
        book_stats.iloc[0]["Title"]
    ),
    "top_book_rating": float(
        book_stats.iloc[0]["avg_rating"]
    ),
    "top_book_review_count": int(
        book_stats.iloc[0]["review_count"]
    ),
    "top_book_weighted_score": float(
        book_stats.iloc[0]["weighted_score"]
    )
}

with open(
    METRICS_OUTPUT,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        metrics,
        f,
        indent=4
    )

print(
    f"Metrics saved to:\n{METRICS_OUTPUT}"
)

# ============================================================
# Preview
# ============================================================

print("\nTop 20 Books")
print("-" * 80)

print(
    book_stats
    .head(TOP_N_PREVIEW)
    .to_string(index=False)
)

print("\nTraining complete.")
