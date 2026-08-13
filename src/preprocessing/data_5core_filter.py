import pandas as pd
from collections import Counter

INPUT_FILE = "Books_rating_trimmed.csv"
OUTPUT_FILE = "books_ratings_5core.csv"

CHUNK_SIZE = 100_000
MIN_USER_REVIEWS = 5
MIN_BOOK_REVIEWS = 5

print("=" * 60)
print("PASS 1: Counting user and book interactions")
print("=" * 60)

user_counts = Counter()
book_counts = Counter()

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=["User_id", "Title"],
    chunksize=CHUNK_SIZE
):
    user_counts.update(chunk["User_id"].dropna())
    book_counts.update(chunk["Title"].dropna())

print(f"Unique users discovered : {len(user_counts):,}")
print(f"Unique books discovered : {len(book_counts):,}")

valid_users = {
    user
    for user, count in user_counts.items()
    if count >= MIN_USER_REVIEWS
}

valid_books = {
    book
    for book, count in book_counts.items()
    if count >= MIN_BOOK_REVIEWS
}

print()
print("=" * 60)
print("5-CORE ELIGIBILITY")
print("=" * 60)

print(f"Users with >= {MIN_USER_REVIEWS} reviews : {len(valid_users):,}")
print(f"Books with >= {MIN_BOOK_REVIEWS} reviews : {len(valid_books):,}")

print()
print("=" * 60)
print("PASS 2: Creating filtered dataset")
print("=" * 60)

first_chunk = True

rows_before = 0
rows_after = 0

for i, chunk in enumerate(
    pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE)
):
    print(f"Processing chunk {i:,}")

    rows_before += len(chunk)

    filtered = chunk[
        chunk["User_id"].isin(valid_users)
        &
        chunk["Title"].isin(valid_books)
    ]

    rows_after += len(filtered)

    filtered.to_csv(
        OUTPUT_FILE,
        mode="w" if first_chunk else "a",
        index=False,
        header=first_chunk
    )

    first_chunk = False
