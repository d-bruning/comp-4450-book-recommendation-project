from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_predict_hobbit():

    response = client.post(
        "/predict",
        json={
            "favorite_book": "The Hobbit",
            "n_recommendations": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["favorite_book"] == "The Hobbit"

    assert len(data["recommendations"]) > 0


def test_predict_invalid_book():

    response = client.post(
        "/predict",
        json={
            "favorite_book": "DefinitelyNotABook123456",
            "n_recommendations": 5
        }
    )

    assert response.status_code == 404
