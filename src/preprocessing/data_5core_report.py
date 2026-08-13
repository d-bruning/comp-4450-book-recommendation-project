import pandas as pd

df = pd.read_csv("books_ratings_5core.csv")

print("=" * 60)
print("5-CORE DATASET SUMMARY")
print("=" * 60)

print(f"Rows         : {len(df):,}")
print(f"Books        : {df['Title'].nunique():,}")
print(f"Users        : {df['User_id'].nunique():,}")

print("\nReviews Per User")
print(df.groupby("User_id").size().describe())

print("\nReviews Per Book")
print(df.groupby("Title").size().describe())

print("\nRating Distribution")
print(df["review/score"].value_counts().sort_index())
