import pandas as pd

FILE = "Books_rating_trimmed.csv"
CHUNK_SIZE = 100_000

titles = set()
users = set()
score_counts = {}
total_rows = 0

for chunk in pd.read_csv(FILE, chunksize=CHUNK_SIZE):
    total_rows += len(chunk)

    titles.update(chunk["Title"].dropna().unique())
    users.update(chunk["User_id"].dropna().unique())

    counts = chunk["review/score"].value_counts()

    for score, count in counts.items():
        score_counts[score] = score_counts.get(score, 0) + count

print("\n===== Dataset Statistics =====")
print(f"Total Rows: {total_rows:,}")
print(f"Unique Titles: {len(titles):,}")
print(f"Unique Users: {len(users):,}")

print("\nReview Score Distribution:")
for score in sorted(score_counts.keys()):
    print(f"{score}: {score_counts[score]}")
