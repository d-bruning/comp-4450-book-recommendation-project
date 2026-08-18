from fastapi import FastAPI, HTTPException

from src.api.cache_service import cache_prediction, get_cached_prediction
from src.api.logging_service import log_prediction
from src.api.recommender import get_recommendations
from src.api.schemas import RecommendationRequest, RecommendationResponse, FeedbackRequest, FeedbackResponse
from src.api.feedback_service import save_feedback

app = FastAPI(
    title="Book Recommender API",
    version="1.0"
)

# ============================================================
# API Health Endpoint
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }

# ============================================================
# Prediction Endpoint
# ============================================================

@app.post(
    "/predict",
    response_model=RecommendationResponse
)
def predict(
    # Generate recommendations using
    # the production recommendation model.
    request: RecommendationRequest
):
    cached = get_cached_prediction(
        request.favorite_book
    )
    # Check for previously generated
    # recommendations before running
    # model inference.
    if cached is not None:

        log_prediction(
            request.favorite_book,
            cached,
            cache_hit=True
        )

        return {
            "favorite_book":
                request.favorite_book,
            "recommendations":
                cached
        }

    recommendations = get_recommendations(
        request.favorite_book,
        request.n_recommendations
    )

    # Persist request activity for
    # monitoring and usage analysis.
    log_prediction(
        request.favorite_book,
        recommendations
    )

    cache_prediction(
        request.favorite_book,
        recommendations
    )

    if recommendations is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "favorite_book":
            request.favorite_book,
        "recommendations":
            recommendations
    }


# ============================================================
# Feedback Endpoint
# ============================================================

@app.post(
    "/feedback",
    response_model=FeedbackResponse
)
def submit_feedback(
    request: FeedbackRequest
):
    """
    Persist user feedback on recommendation quality.
    Feedback is used to calculate live recommendation usefulness metrics within the monitoring dashboard.
    """
    save_feedback(
        request.favorite_book,
        request.feedback,
        request.recommendation_count
    )

    return {
        "status": "recorded"
    }
