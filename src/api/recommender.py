import ast
import re
from pathlib import Path

import joblib
import pandas as pd

# ============================================================
# Book Recommendation Engine
# ============================================================
#
# Loads the production KNN collaborative filtering model and
# associated metadata required to generate book recommendations.
#
# Responsibilities:
# - Load trained model artifacts
# - Normalize book titles
# - Enrich recommendations with metadata
# - Generate author and cover information
# - Return nearest-neighbor recommendations
#
# ============================================================

# ============================================================
# Base Configuration
# ============================================================

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
    / "processed"
    / "books_metadata.csv"
)

# Metadata lookup structure used to enrich recommendation
# results with author names and cover images.
metadata_lookup = {}

model = None
book_index = []
book_lookup = {}

def clean_authors(value):
    """
    Format author metadata for display.

    Goodreads and Amazon metadata occasionally contain serialized lists of any
    combination of authors, editors, edition info, publishers, etc. This
    function truncates excessively long lists.
    """

    if pd.isna(value):

        return "Unknown Author"

    try:

        parsed = ast.literal_eval(value)

        if isinstance(parsed, list):

            if len(parsed) <= 3:

                return ", ".join(parsed)

            return ", ".join(parsed[:3]) + "..."

    except (
        ValueError,
        SyntaxError,
    ):

        pass

    return str(value)

# Load metadata used to enrich recommendation results. This information is not
# required for inference but significantly improves the frontend user experience.
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

# Load production model artifacts and create a case-insensitive lookup index
# for book titles.
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
    """
    Normalize titles to reduce duplicate recommendations.

    Many books appear multiple times in the source data with subtitles,
    alternate editions, or formatting differences. Normalization helps prevent
    the same book from being recommended multiple times.
    """
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
    """
    Generate book recommendations using the trained item-based KNN
    collaborative filtering model.

    Workflow:
    1. Validate model availability.
    2. Locate the requested book.
    3. Query nearest neighbors.
    4. Remove duplicate editions.
    5. Enrich results with metadata.
    6. Return recommendation list.
    """

    # Model artifacts must be available before recommendations can be generated.
    if (
        model is None
        or not book_lookup
    ):

        return None
    lookup_title = book_title.lower()

    # Return None when the requested title is
    # not present in the trained recommendation index.
    if lookup_title not in book_lookup:
        return None

    idx = book_lookup[lookup_title]

    # Retrieve a larger candidate set than ultimately needed. This helps
    # address duplicate titles and alternate editions that may be removed
    # during post-processing.
    search_size = max(
        50,
        n * 10
    )


    # Query nearest-neighbor books from the trained model.
    _distances, indices = model.kneighbors(
        model._fit_X[idx],
        n_neighbors=search_size
    )

    recommendations = []

    # Track normalized titles to prevent duplicate recommendations representing
    # the same book.
    seen = {normalize_title(book_title)}

    for neighbor_idx in indices.flatten():

        candidate = book_index[neighbor_idx]

        normalized = normalize_title(candidate)

        if normalized in seen:
            continue

        seen.add(normalized)

        # Enrich recommendations with author and cover image metadata for
        # frontend display.
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

        # Stop once the requested number of recommendations has been collected.
        if len(recommendations) >= n:
            break

    return recommendations
