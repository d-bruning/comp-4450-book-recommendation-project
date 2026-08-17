import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from src.training.mlflow_utils import get_git_commit

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

MIN_BOOK_REVIEWS = 10
POSITIVE_THRESHOLD = 5

EXPERIMENT_NAME = "COMP4450 Book Recommender"
RUN_NAME = "item_knn_v3"
DATASET_VERSION = "books_ratings_5core_v1"

# ============================================================
# MLflow
# ============================================================

mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run(run_name=RUN_NAME):

    mlflow.log_params(
        {
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

    # ========================================================
    # Positive interactions
    # ========================================================

    df = df[
        df["review/score"] >= POSITIVE_THRESHOLD
    ]

    # ========================================================
    # Remove low-volume books
    # ========================================================

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

    print(
        f"Books retained: "
        f"{df['Title'].nunique():,}"
    )

    # ========================================================
    # Item-user matrix
    # ========================================================

    book_user_matrix = pd.crosstab(
        df["Title"],
        df["User_id"]
    )

    sparse_matrix = csr_matrix(
        book_user_matrix.values
    )

    # ========================================================
    # Train KNN
    # ========================================================

    model = NearestNeighbors(
        metric="cosine",
        algorithm="brute",
        n_neighbors=20
    )

    model.fit(sparse_matrix)

    # ========================================================
    # Save Artifacts
    # ========================================================

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
        "books_used":
            int(df["Title"].nunique()),
        "users_used":
            int(df["User_id"].nunique()),
        "interactions_used":
            len(df)
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

    # ========================================================
    # Metrics
    # ========================================================

    density = (
        sparse_matrix.nnz
        /
        (
            sparse_matrix.shape[0]
            * sparse_matrix.shape[1]
        )
    )

    mlflow.log_metrics(
        {
            "books_used":
                metadata["books_used"],
            "users_used":
                metadata["users_used"],
            "interactions_used":
                metadata["interactions_used"],
            "matrix_density":
                density
        }
    )

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="book-recommender-knn"
    )

    mlflow.log_artifact(str(BOOK_INDEX_FILE))
    mlflow.log_artifact(str(METADATA_FILE))

print("Item KNN training complete.")
