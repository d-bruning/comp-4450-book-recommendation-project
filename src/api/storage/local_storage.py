from pathlib import Path
from datetime import datetime, timezone
import json

PROJECT_ROOT = Path(__file__).resolve().parents[3]

LOG_FILE = (
    PROJECT_ROOT
    / "logs"
    / "prediction_logs.jsonl"
)

CACHE_FILE = (
    PROJECT_ROOT
    / "logs"
    / "recommendation_cache.json"
)

LOG_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

from pathlib import Path
from datetime import datetime, timezone
import json

PROJECT_ROOT = Path(__file__).resolve().parents[3]

LOG_FILE = (
    PROJECT_ROOT
    / "logs"
    / "prediction_logs.jsonl"
)

CACHE_FILE = (
    PROJECT_ROOT
    / "logs"
    / "recommendation_cache.json"
)

LOG_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Create cache file if missing

if not CACHE_FILE.exists():

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {},
            f,
            indent=4
        )


def log_prediction(
    favorite_book,
    recommendations,
    cache_hit=False
):

    record = {
        "timestamp": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "favorite_book": favorite_book,
        "cache_hit": cache_hit,
        "recommendations": recommendations
    }

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(record)
        )

        f.write("\n")

def get_cached_prediction(
    favorite_book
):

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            cache = json.load(f)

        return cache.get(
            favorite_book.lower()
        )

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        return None

def cache_prediction(
    favorite_book,
    recommendations
):

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            cache = json.load(f)

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        cache = {}

    cache[
        favorite_book.lower()
    ] = recommendations

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cache,
            f,
            indent=4
        )
