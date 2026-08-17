import os
from pathlib import Path

import joblib
import requests
import streamlit as st

# ============================================================
# Configuration
# ============================================================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

ASSETS_DIR = (
    Path(__file__).parent
    / "assets"
)

DEFAULT_IMAGE = (
    ASSETS_DIR
    / "default-book.svg"
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BOOK_INDEX_FILE = (
    PROJECT_ROOT
    / "models"
    / "book_index.joblib"
)

book_titles = sorted(
    joblib.load(BOOK_INDEX_FILE)
)

# ============================================================
# Session State
# ============================================================

if "recommendations" not in st.session_state:

    st.session_state["recommendations"] = []

if "favorite_book" not in st.session_state:

    st.session_state["favorite_book"] = None

# ============================================================
# Page
# ============================================================

st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

st.title(
    "Get Recc'd: A Book Recommendation System"
)

st.write(
    "Enter a favorite book to receive similar recommendations."
)

# ============================================================
# Inputs
# ============================================================

favorite_book = st.selectbox(
    "Favorite Book",
    options=book_titles,
    index=None,
    placeholder="Select a book..."
)

# ============================================================
# Recommendation Request
# ============================================================

if st.button(
    "Get Recommendations"
):

    if not favorite_book:

        st.error(
            "Please enter a book title."
        )

    else:

        try:

            response = requests.post(
                f"{API_URL}/predict",
                json={
                    "favorite_book":
                        favorite_book,
                    "n_recommendations":
                        5
                },
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                st.session_state[
                    "favorite_book"
                ] = favorite_book

                st.session_state[
                    "recommendations"
                ] = result.get(
                    "recommendations",
                    []
                )

            elif response.status_code == 404:

                st.error(
                    "Book not found."
                )

            else:

                st.error(
                    f"API Error: "
                    f"{response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to FastAPI."
                "\n\nMake sure the API is running:"
                "\n\nuvicorn src.api.main:app --reload"
            )

        except Exception as e:

            st.error(str(e))

# ============================================================
# Display Recommendations
# ============================================================

recommendations = (
    st.session_state[
        "recommendations"
    ]
)

selected_book = (
    st.session_state[
        "favorite_book"
    ]
)

if recommendations:

    st.success(
        f"Recommendations based on "
        f"'{selected_book}'"
    )

    for recommendation in recommendations:

        title = recommendation.get(
            "title",
            "Unknown Title"
        )

        author = recommendation.get(
            "author",
            "Unknown Author"
        )

        image = recommendation.get(
            "image"
        )

        col1, col2 = st.columns(
            [1, 4]
        )

        with col1:

            if image:

                st.image(
                    image,
                    width=100
                )

            else:

                st.image(
                    str(DEFAULT_IMAGE),
                    width=100
                )

        with col2:

            st.subheader(title)

            st.write(
                f"Author: {author}"
            )

        st.divider()

    # ========================================================
    # Feedback Section
    # ========================================================

    st.subheader(
        "Recommendation Feedback"
    )

    st.write(
        "Were these recommendations helpful?"
    )

    feedback = st.radio(
        "Feedback",
        [
            "positive",
            "negative"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    if st.button(
        "Submit Feedback"
    ):

        try:

            feedback_payload = {

                "favorite_book":
                    selected_book,

                "feedback":
                    feedback,

                "recommendation_count":
                    len(
                        recommendations
                    )
            }

            response = requests.post(
                f"{API_URL}/feedback",
                json=feedback_payload,
                timeout=10
            )

            if response.ok:

                st.success(
                    "Feedback submitted."
                )

            else:

                st.error(
                    "Unable to submit feedback."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to FastAPI."
            )

        except Exception as e:

            st.error(
                str(e)
            )
