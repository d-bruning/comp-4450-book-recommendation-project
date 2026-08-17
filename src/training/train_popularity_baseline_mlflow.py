import json
import subprocess
from pathlib import Path

import mlflow
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

EXPERIMENT_NAME = "COMP4450 Book Recommender"
RUN_NAME = "popularity_baseline_v1"
DATASET_VERSION = "books_ratings_5core_v1"

# ============================================================
# Helpers
# ============================================================

def get_git_commit():
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"]
            )
            .decode("utf-8")
            .strip()
        )
    except Exception:
        return "unknown"

# ============================================================
# Directories
# ============================================================

MODEL_OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

METRICS_OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

# ============================================================
# MLflow
# ============================================================

mlflow.set_experiment(EXPERIMENT_NAME)
print("Starting MLflow run...")

with mlflow.start_run(run_name=RUN_NAME):

    mlflow.log_params(
        {
            "model_type": "popularity_baseline",
            "minimum_reviews": MIN_REVIEWS,
            "dataset_version": DATASET_VERSION,
            "git_commit": get_git_commit(),
        }
    )

    # ============================================================
    # Load Dataset
    # ============================================================

    print("Loading dataset...")

    df = pd.read_csv(
        INPUT_FILE,
        usecols=[
            "Title",
            "review/score"
        ]
    )

    print(f"Loaded {len(df):,} reviews")

    # ============================================================
    # Aggregate Statistics
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
    # Filter
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
    # Weighted Score
    # ============================================================

    book_stats["weighted_score"] = (
        book_stats["avg_rating"]
        * np.log10(book_stats["review_count"])
    )

    # ============================================================
    # Formatting
    # ============================================================

    book_stats["avg_rating"] = (
        book_stats["avg_rating"].round(3)
    )

    book_stats["positive_pct"] = (
        book_stats["positive_pct"].round(2)
    )

    book_stats["review_pct"] = (
        book_stats["review_pct"].round(4)
    )

    book_stats["weighted_score"] = (
        book_stats["weighted_score"].round(3)
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
    # Save Model
    # ============================================================

    book_stats.to_csv(
        MODEL_OUTPUT,
        index=False
    )

    mlflow.log_artifact(
        str(MODEL_OUTPUT)
    )

    # ============================================================
    # Metrics
    # ============================================================

    positive_interactions = (
        df["review/score"] >= 4
    ).sum()

    metrics = {
        "dataset_reviews": len(df),
        "dataset_books": int(df["Title"].nunique()),
        "eligible_books": len(book_stats),
        "positive_interaction_ratio_pct": round(
            (
                positive_interactions
                / len(df)
            ) * 100,
            2
        ),

        # New metrics
        "top_book_rating": float(
            book_stats.iloc[0]["avg_rating"]
        ),

        "top_book_review_count": int(
            book_stats.iloc[0]["review_count"]
        ),

        "top_book_weighted_score": float(
            book_stats.iloc[0]["weighted_score"]
        ),

        "avg_weighted_score": round(
            float(
                book_stats["weighted_score"].mean()
            ),
            3
        ),

        "max_weighted_score": round(
            float(
                book_stats["weighted_score"].max()
            ),
            3
        )
    }

    print("Logging metrics...")
    mlflow.log_metrics(metrics)

    report = {
        **metrics,
        "top_book": book_stats.iloc[0]["Title"],
        "top_book_rating": float(
            book_stats.iloc[0]["avg_rating"]
        ),
        "top_book_review_count": int(
            book_stats.iloc[0]["review_count"]
        ),
    }

    with open(
        METRICS_OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            report,
            f,
            indent=4
        )

    print("Logging artifacts...")
    mlflow.log_artifact(
        str(METRICS_OUTPUT)
    )

print("Baseline training complete.")
