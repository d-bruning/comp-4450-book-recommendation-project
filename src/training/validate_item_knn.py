import re
from pathlib import Path

import joblib
import pandas as pd
from scipy.sparse import csr_matrix

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

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "item_knn_model.joblib"
)

BOOK_INDEX_FILE = (
    PROJECT_ROOT
    / "models"
    / "book_index.joblib"
)

MIN_BOOK_REVIEWS = 20
POSITIVE_THRESHOLD = 4

# ============================================================
# Load Model Assets
# ============================================================

print("Loading model...")

model = joblib.load(MODEL_FILE)
book_index = joblib.load(BOOK_INDEX_FILE)

print(f"Loaded {len(book_index):,} books")

# ============================================================
# Rebuild Matrix
# ============================================================

print("Loading dataset...")

df = pd.read_csv(
    INPUT_FILE,
    usecols=[
        "Title",
        "User_id",
        "review/score"
    ]
)

df = df[
    df["review/score"] >= POSITIVE_THRESHOLD
]

book_counts = df.groupby("Title").size()

valid_books = book_counts[
    book_counts >= MIN_BOOK_REVIEWS
].index

df = df[
    df["Title"].isin(valid_books)
]

book_user_matrix = pd.crosstab(
    df["Title"],
    df["User_id"]
)

sparse_matrix = csr_matrix(
    book_user_matrix.values
)

# ============================================================
# Recommendation Function
# ============================================================

def normalize_title(title: str) -> str:
    title = title.lower()

    # Remove punctuation
    title = re.sub(r"[^a-z0-9 ]", " ", title)

    # Common edition/subtitle cleanup
    remove_phrases = [
        "or there and back again",
        "there and back again",
        "illustrated by the author",
        "bbc audio collection",
        "large print",
        "2nd edition",
        "edition",
        " or "
    ]

    for phrase in remove_phrases:
        title = title.replace(phrase, "")

    title = title.replace("hobbitt", "hobbit")
    title = re.sub(r"\s+", " ", title)

    return title.strip()

def recommend(book_title, n=10):

    if book_title not in book_user_matrix.index:
        print(f"\nBook not found: {book_title}")
        return

    idx = book_user_matrix.index.get_loc(book_title)

    distances, indices = model.kneighbors(
        sparse_matrix[idx],
        n_neighbors=n + 1
    )

    print(f"\nRecommendations for '{book_title}'")
    print("-" * 80)

    recommendations_found = 0

    seen_titles = {
        normalize_title(book_title)
    }

    for distance, neighbor_idx in zip(
        distances.flatten(),
        indices.flatten()
    ):

        neighbor_title = (
            book_user_matrix.index[neighbor_idx]
        )

        normalized = normalize_title(
            neighbor_title
        )

        if normalized in seen_titles:
            continue

        seen_titles.add(normalized)

        similarity = 1 - distance

        recommendations_found += 1

        print(
            f"{recommendations_found:2d}. "
            f"{neighbor_title} "
            f"(normalized='{normalized}') "
            f"(similarity={similarity:.3f})"
        )

# ============================================================
# Test Books
# ============================================================

recommend("The Hobbit")

# Uncomment additional tests

# recommend("Pride and Prejudice")
# recommend("Jane Eyre")
# recommend("Brave New World")
