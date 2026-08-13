from fastapi import FastAPI
from fastapi import HTTPException

from src.api.schemas import (
    RecommendationRequest,
    RecommendationResponse
)

from src.api.recommender import (
    get_recommendations
)

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

    recommendations = get_recommendations(
        request.favorite_book,
        request.n_recommendations
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
