import pandas as pd
from pathlib import Path

INPUT_FILE = "books_ratings_5core.csv"

print("=" * 80)
print("BOOK RECOMMENDER DATASET PROFILE")
print("=" * 80)

# ------------------------------------------------------------------
# Load dataset
# ------------------------------------------------------------------

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

# ------------------------------------------------------------------
# General Statistics
# ------------------------------------------------------------------

rows = len(df)
books = df["Title"].nunique()
users = df["User_id"].nunique()

print("\nGENERAL STATISTICS")
print("-" * 80)

print(f"Rows                : {rows:,}")
print(f"Unique Books        : {books:,}")
print(f"Unique Users        : {users:,}")

print(f"Avg Reviews / Book  : {rows / books:.2f}")
print(f"Avg Reviews / User  : {rows / users:.2f}")

# ------------------------------------------------------------------
# Memory Usage
# ------------------------------------------------------------------

print("\nMEMORY USAGE")
print("-" * 80)

memory_mb = df.memory_usage(deep=True).sum() / 1024**2

print(f"Dataset Size in RAM : {memory_mb:.2f} MB")

# ------------------------------------------------------------------
# Missing Values
# ------------------------------------------------------------------

print("\nMISSING VALUES")
print("-" * 80)

missing = df.isnull().sum()

for col, count in missing.items():
    pct = count / rows * 100
    print(f"{col:<20} {count:>10,} ({pct:.2f}%)")

# ------------------------------------------------------------------
# Rating Distribution
# ------------------------------------------------------------------

print("\nRATING DISTRIBUTION")
print("-" * 80)

rating_dist = df["review/score"].value_counts().sort_index()

for rating, count in rating_dist.items():
    pct = count / rows * 100
    print(f"{rating:.1f} Stars : {count:>10,} ({pct:.2f}%)")

# ------------------------------------------------------------------
# User Activity
# ------------------------------------------------------------------

print("\nUSER ACTIVITY")
print("-" * 80)

user_reviews = df.groupby("User_id").size()

print(user_reviews.describe())

# ------------------------------------------------------------------
# Book Popularity
# ------------------------------------------------------------------

print("\nBOOK POPULARITY")
print("-" * 80)

book_reviews = df.groupby("Title").size()

print(book_reviews.describe())

# ------------------------------------------------------------------
# Sparsity
# ------------------------------------------------------------------

print("\nSPARSITY ANALYSIS")
print("-" * 80)

possible_interactions = users * books
actual_interactions = rows

sparsity = (
    1 - (actual_interactions / possible_interactions)
) * 100

print(f"Possible Interactions : {possible_interactions:,}")
print(f"Actual Interactions   : {actual_interactions:,}")
print(f"Sparsity              : {sparsity:.6f}%")

# ------------------------------------------------------------------
# Long Tail Books
# ------------------------------------------------------------------

print("\nLONG TAIL ANALYSIS")
print("-" * 80)

under_5 = (book_reviews < 5).sum()
under_10 = (book_reviews < 10).sum()
under_20 = (book_reviews < 20).sum()

print(f"Books with < 5 reviews  : {under_5:,}")
print(f"Books with <10 reviews  : {under_10:,}")
print(f"Books with <20 reviews  : {under_20:,}")

# ------------------------------------------------------------------
# Top Books
# ------------------------------------------------------------------

print("\nTOP 20 MOST REVIEWED BOOKS")
print("-" * 80)

top_books = (
    df.groupby("Title")
      .size()
      .sort_values(ascending=False)
      .head(20)
)

for title, count in top_books.items():
    print(f"{count:>8,} | {title}")

# ------------------------------------------------------------------
# Top Users
# ------------------------------------------------------------------

print("\nTOP 20 MOST ACTIVE USERS")
print("-" * 80)

top_users = user_reviews.sort_values(
    ascending=False
).head(20)

for user, count in top_users.items():
    print(f"{count:>8,} | {user}")

# ------------------------------------------------------------------
# Positive vs Negative
# ------------------------------------------------------------------

print("\nPOSITIVE INTERACTIONS")
print("-" * 80)

positive = (df["review/score"] >= 4).sum()
negative = (df["review/score"] < 4).sum()

print(f"Positive (4-5 stars) : {positive:,}")
print(f"Negative (1-3 stars) : {negative:,}")

print(
    f"Positive Ratio       : "
    f"{positive / rows * 100:.2f}%"
)

# ------------------------------------------------------------------
# Export Summary
# ------------------------------------------------------------------

summary = pd.DataFrame(
    [
        {
            "rows": rows,
            "books": books,
            "users": users,
            "avg_reviews_per_book": rows / books,
            "avg_reviews_per_user": rows / users,
            "sparsity_pct": sparsity,
            "positive_ratio_pct": positive / rows * 100,
        }
    ]
)

summary.to_csv(
    "dataset_profile_summary.csv",
    index=False
)

print("\nSummary written to:")
print(Path("dataset_profile_summary.csv").resolve())

print("\nDone.")
