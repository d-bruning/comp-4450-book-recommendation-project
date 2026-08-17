from fastapi import FastAPI, HTTPException

from src.api.cache_service import cache_prediction, get_cached_prediction
from src.api.logging_service import log_prediction
from src.api.recommender import get_recommendations
from src.api.schemas import RecommendationRequest, RecommendationResponse

app = FastAPI(
    title="Book Recommender API",
    version="1.0"
)


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.post(
    "/predict",
    response_model=RecommendationResponse
)
def predict(
    request: RecommendationRequest
):
    cached = get_cached_prediction(
        request.favorite_book
    )

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
