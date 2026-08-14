from pathlib import Path
import re

import joblib
import ast
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

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
    / "data"
    / "raw"
    / "books_data.csv"
)

metadata_lookup = {}

model = None
book_index = []
book_lookup = {}

def clean_authors(value):
    if pd.isna(value):
        return "Unknown Author"

    try:
        parsed = ast.literal_eval(value)

        if isinstance(parsed, list):

            # keep legitimate author lists
            if len(parsed) <= 3:
                return ", ".join(parsed)

            # likely contributor explosion
            return ", ".join(parsed[:3]) + "..."

    except Exception:
        pass

    return str(value)

if METADATA_FILE.exists():

    metadata_df = pd.read_csv(
        METADATA_FILE,
        usecols=[
            "Title",
            "authors",
            "image"
        ]
    )

    metadata_df["authors"] = (
        metadata_df["authors"]
        .apply(clean_authors)
    )

    metadata_lookup = (
        metadata_df
        .drop_duplicates("Title")
        .set_index("Title")
        .to_dict("index")
    )


if (
    MODEL_FILE.exists()
    and BOOK_INDEX_FILE.exists()
):

    model = joblib.load(
        MODEL_FILE
    )

    book_index = joblib.load(
        BOOK_INDEX_FILE
    )

    book_lookup = {
        title.lower(): idx
        for idx, title
        in enumerate(book_index)
    }


def normalize_title(title: str) -> str:
    title = title.lower()

    title = re.sub(r"[^a-z0-9 ]", " ", title)

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




def get_recommendations(
    book_title: str,
    n: int = 10
):
    if (
        model is None
        or not book_lookup
    ):

        return None
    lookup_title = book_title.lower()

    if lookup_title not in book_lookup:
        return None

    idx = book_lookup[lookup_title]

    search_size = max(
        50,
        n * 10
    )

    distances, indices = model.kneighbors(
        model._fit_X[idx],
        n_neighbors=search_size
    )

    recommendations = []

    seen = {normalize_title(book_title)}

    for neighbor_idx in indices.flatten():

        candidate = book_index[neighbor_idx]

        normalized = normalize_title(candidate)

        if normalized in seen:
            continue

        seen.add(normalized)

        metadata = metadata_lookup.get(
            candidate,
            {}
        )

        image = metadata.get("image")

        if pd.isna(image):
            image = None

        recommendations.append(
            {
                "title": candidate,
                "author": metadata.get(
                    "authors",
                    "Unknown Author"
                ),
                "image": image
            }
        )

        if len(recommendations) >= n:
            break

    return recommendations
