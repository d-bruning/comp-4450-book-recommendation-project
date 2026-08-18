import boto3
import uuid
import pandas as pd
from datetime import datetime, timezone

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1"
)

prediction_table = dynamodb.Table(
    "prediction-history"
)

cache_table = dynamodb.Table(
    "recommendation-cache"
)

feedback_table = dynamodb.Table(
    "recommendation-feedback"
)


def log_prediction(
    favorite_book,
    recommendations,
    cache_hit=False
):

    prediction_table.put_item(
        Item={
            "prediction_id": str(
                uuid.uuid4()
            ),
            "timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            "favorite_book":
                favorite_book,
            "cache_hit":
                cache_hit,
            "recommendations":
                recommendations
        }
    )


def get_cached_prediction(
    favorite_book
):

    response = cache_table.get_item(
        Key={
            "favorite_book":
                favorite_book.lower()
        }
    )

    item = response.get(
        "Item"
    )

    if item:

        return item.get(
            "recommendations"
        )

    return None


def cache_prediction(
    favorite_book,
    recommendations
):

    if recommendations is None:
        return

    cache_table.put_item(
        Item={
            "favorite_book":
                favorite_book.lower(),
            "cached_at": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            "recommendations":
                recommendations
        }
    )

def save_feedback(
    favorite_book: str,
    feedback: str,
    recommendation_count: int
):

    feedback_table.put_item(
        Item={
            "feedback_id": str(uuid.uuid4()),
            "favorite_book": favorite_book,
            "feedback": feedback,
            "recommendation_count": recommendation_count,
            "timestamp": (
                datetime.now(timezone.utc)
                .isoformat()
            )
        }
    )


def load_feedback():

    response = feedback_table.scan()

    items = response.get(
        "Items",
        []
    )

    if not items:
        return pd.DataFrame()

    df = pd.DataFrame(items)

    if "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

    return df
