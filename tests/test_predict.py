from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_predict_invalid_book():

    response = client.post(
        "/predict",
        json={
            "favorite_book": "DefinitelyNotABook123456",
            "n_recommendations": 5
        }
    )

    assert response.status_code == 404
