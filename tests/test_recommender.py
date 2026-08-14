from src.api.recommender import get_recommendations


def test_recommendations_return_results():

    recommendations = get_recommendations(
        "The Hobbit",
        5
    )

    assert recommendations is not None

    assert len(recommendations) > 0


def test_recommendation_structure():

    recommendations = get_recommendations(
        "The Hobbit",
        5
    )

    recommendation = recommendations[0]

    assert "title" in recommendation
    assert "author" in recommendation
    assert "image" in recommendation


def test_invalid_book_returns_none():

    recommendations = get_recommendations(
        "DefinitelyNotABook123456",
        5
    )

    assert recommendations is None
