from pathlib import Path
import json

import pandas as pd

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


def load_prediction_logs():

    records = []

    if not LOG_FILE.exists():
        return pd.DataFrame()

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:

                records.append(
                    json.loads(line)
                )

            except json.JSONDecodeError:
                pass

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    if "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

    return df


def load_cache():

    if not CACHE_FILE.exists():
        return {}

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {}
