from pathlib import Path
import json
import pandas as pd

# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "models"
    / "popularity_baseline.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "models"
    / "popularity_baseline_top100.csv"
)

METRICS_OUTPUT = (
    PROJECT_ROOT
    / "artifacts"
    / "reports"
    / "popularity_baseline_top100_metrics.json"
)

TOP_N = 100

# ============================================================
# Create Directories
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

METRICS_OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

# ============================================================
# Load Baseline Model
# ============================================================

print("Loading popularity baseline...")

df = pd.read_csv(INPUT_FILE)

print(f"Loaded {len(df):,} ranked books")

# ============================================================
# Generate Top 100
# ============================================================

top_books = df.head(TOP_N)

top_books.to_csv(
    OUTPUT_FILE,
    index=False
)

# ============================================================
# Metrics
# ============================================================

metrics = {
    "top_n": TOP_N,
    "books_in_output": len(top_books),
    "top_book": str(top_books.iloc[0]["Title"]),
    "top_book_rating": float(
        top_books.iloc[0]["avg_rating"]
    ),
    "top_book_review_count": int(
        top_books.iloc[0]["review_count"]
    ),
    "top_book_weighted_score": float(
        top_books.iloc[0]["weighted_score"]
    ),
    "avg_rating_top100": round(
        float(top_books["avg_rating"].mean()),
        3
    ),
    "avg_weighted_score_top100": round(
        float(top_books["weighted_score"].mean()),
        3
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

# ============================================================
# Preview
# ============================================================

print(f"\nSaved Top {TOP_N} books:")
print(OUTPUT_FILE)

print(f"\nMetrics saved:")
print(METRICS_OUTPUT)

print("\nTop 10 Books")
print("-" * 80)

print(
    top_books.head(10).to_string(
        index=False
    )
)

print("\nTop 100 generation complete.")
