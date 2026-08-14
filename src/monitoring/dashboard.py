from pathlib import Path
import json

import pandas as pd
import streamlit as st

# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

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

# ============================================================
# Helpers
# ============================================================

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


# ============================================================
# Load Data
# ============================================================

log_df = load_prediction_logs()

cache_data = load_cache()

# ============================================================
# Page
# ============================================================

st.set_page_config(
    page_title="Monitoring Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("Book Recommendation Monitoring Dashboard")

st.write(
    "Operational monitoring for the Book Recommendation System."
)

# ============================================================
# Metrics
# ============================================================

total_predictions = (
    len(log_df)
    if not log_df.empty
    else 0
)

unique_books = (
    log_df["favorite_book"].nunique()
    if not log_df.empty
    else 0
)

cache_entries = len(cache_data)
cache_hits = 0
cache_misses = 0
cache_hit_rate = 0
most_requested_book = "N/A"

if not log_df.empty:

    if "cache_hit" not in log_df.columns:
        log_df["cache_hit"] = False

    cache_hits = (
        log_df["cache_hit"]
        .sum()
    )

    cache_misses = (
        len(log_df)
        - cache_hits
    )

    if len(log_df) > 0:

        cache_hit_rate = round(
            (
                cache_hits
                / len(log_df)
            ) * 100,
            1
        )

    most_requested_book = (
        log_df["favorite_book"]
        .value_counts()
        .idxmax()
    )



col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Predictions",
        total_predictions
    )

with col2:
    st.metric(
        "Unique Books",
        unique_books
    )

with col3:
    st.metric(
        "Cache Hit Rate",
        f"{cache_hit_rate}%"
    )

with col4:
    st.metric(
        "Most Requested Book",
        most_requested_book
    )

with col5:
    st.metric(
        "Cached Books",
        cache_entries
    )

# ============================================================
# Request Trends
# ============================================================

st.subheader("Prediction Volume")

if not log_df.empty:

    trend_df = (
        log_df
        .groupby(
            log_df["timestamp"].dt.floor("h")
        )
        .size()
        .reset_index(
            name="predictions"
        )
    )

    trend_df = trend_df.set_index(
        "timestamp"
    )

    st.line_chart(
        trend_df["predictions"]
    )

else:

    st.info(
        "No prediction data available."
    )

# ============================================================
# Top Requested Books
# ============================================================

st.subheader("Top Requested Books")

if not log_df.empty:

    book_counts = (
        log_df["favorite_book"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(book_counts)

else:

    st.info(
        "No prediction data available."
    )

# ============================================================
# Cache Content
# ============================================================

st.subheader("Cache Summary")

if cache_data:

    cache_df = pd.DataFrame(
        [
            {
                "Book": book,
                "Recommendation Count":
                    len(recommendations)
            }
            for book, recommendations
            in cache_data.items()
            if recommendations is not None
        ]
    )

    st.dataframe(
        cache_df,
        width="stretch"
    )

else:

    st.info(
        "Cache is empty."
    )

# ============================================================
# Recent Requests
# ============================================================

st.subheader("Recent Requests")

if not log_df.empty:

    recent_df = log_df.copy()

    recent_df[
        "recommendation_count"
    ] = (
        recent_df["recommendations"]
        .apply(
            lambda x: len(x)
            if isinstance(x, list)
            else 0
        )
    )

    recent_df = recent_df[
        [
            "timestamp",
            "favorite_book",
            "recommendation_count"
        ]
    ]

    recent_df = recent_df.sort_values(
        "timestamp",
        ascending=False
    )

    st.dataframe(
        recent_df.head(20),
        width="stretch"
    )

else:

    st.info(
        "No requests logged yet."
    )

# ============================================================
# Raw Log Data
# ============================================================

with st.expander(
    "View Raw Prediction Logs"
):

    if not log_df.empty:

        display_df = log_df.drop(
            columns=["recommendations"],
            errors="ignore"
        )

        st.dataframe(
            display_df,
            width="stretch"
        )

    else:

        st.info(
            "No logs available."
        )
