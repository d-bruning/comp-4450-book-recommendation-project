from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    favorite_book: str
    n_recommendations: int = 10

class BookRecommendation(BaseModel):
    title: str
    author: str
    image: str | None = None

class FeedbackRequest(BaseModel):
    favorite_book: str
    feedback: str
    recommendation_count: int

class FeedbackResponse(BaseModel):
    status: str

class RecommendationResponse(BaseModel):
    favorite_book: str
    recommendations: list[BookRecommendation]
