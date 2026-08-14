import streamlit as st
import requests
from pathlib import Path
import joblib

# ============================================================
# Configuration
# ============================================================

API_URL = "http://127.0.0.1:8000"

DEFAULT_IMAGE = (
    "https://upload.wikimedia.org/"
    "wikipedia/commons/8/87/"
    "Book_icon_1.svg"
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
# Page
# ============================================================

st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

st.title("Get Recc'd: A Book Recommendation System")

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

# recommendation_count = st.slider(
#    "Number of Recommendations",
#    min_value=1,
#    max_value=10,
#    value=5
#)

# ============================================================
# Request
# ============================================================

if st.button("Get Recommendations"):

    if not favorite_book:

        st.error(
            "Please enter a book title."
        )

    else:

        try:

            response = requests.post(
                f"{API_URL}/predict",
                json={
                    "favorite_book": favorite_book,
                    "n_recommendations": 5 # recommendation_count
                },
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    f"Recommendations based on "
                    f"'{favorite_book}'"
                )

                recommendations = (
                    result["recommendations"]
                )

                if not recommendations:

                    st.warning(
                        "No recommendations found."
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
