from pathlib import Path
import json
import subprocess

import joblib
import pandas as pd
import wandb

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

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

METADATA_FILE = (
    PROJECT_ROOT
    / "models"
    / "item_knn_metadata.json"
)

ENTITY = "university-of-denver"
PROJECT = "comp-4450-book-recommendation-project"

MIN_BOOK_REVIEWS = 20
POSITIVE_THRESHOLD = 4

RUN_NAME = "item_knn_production_v1"
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
# W&B
# ============================================================

wandb.init(
    entity=ENTITY,
    project=PROJECT,
    name=RUN_NAME,
    config={
        "model_type": "item_knn",
        "min_book_reviews": MIN_BOOK_REVIEWS,
        "positive_threshold": POSITIVE_THRESHOLD,
        "dataset_version": DATASET_VERSION,
        "git_commit": get_git_commit()
    }
)

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

book_counts = (
    df.groupby("Title")
    .size()
)

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

model = NearestNeighbors(
    metric="cosine",
    algorithm="brute",
    n_neighbors=20
)

model.fit(sparse_matrix)

MODEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)

joblib.dump(
    list(book_user_matrix.index),
    BOOK_INDEX_FILE
)

metadata = {
    "books_used": int(df["Title"].nunique()),
    "users_used": int(df["User_id"].nunique()),
    "interactions_used": int(len(df)),
    "min_book_reviews": MIN_BOOK_REVIEWS,
    "positive_threshold": POSITIVE_THRESHOLD
}

with open(
    METADATA_FILE,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        metadata,
        f,
        indent=4
    )

density = (
    sparse_matrix.nnz
    /
    (
        sparse_matrix.shape[0]
        * sparse_matrix.shape[1]
    )
)

wandb.log(
    {
        "books_used": metadata["books_used"],
        "users_used": metadata["users_used"],
        "interactions_used": metadata["interactions_used"],
        "matrix_density": density
    }
)

artifact = wandb.Artifact(
    name="book-recommender-knn",
    type="model"
)

artifact.add_file(str(MODEL_FILE))
artifact.add_file(str(BOOK_INDEX_FILE))
artifact.add_file(str(METADATA_FILE))

wandb.log_artifact(artifact)

wandb.finish()

print("Item KNN training complete.")
