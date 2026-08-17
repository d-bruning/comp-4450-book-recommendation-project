import boto3
import pandas as pd

# ============================================================
# Configuration
# ============================================================

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

# ============================================================
# Prediction Logs
# ============================================================

def load_prediction_logs():

    try:

        response = prediction_table.scan()

        records = response.get(
            "Items",
            []
        )

        if not records:
            return pd.DataFrame()

        df = pd.DataFrame(records)

        if "timestamp" in df.columns:

            df["timestamp"] = pd.to_datetime(
                df["timestamp"]
            )

        return df

    except Exception as e:

        print(
            f"Failed to load prediction logs: {e}"
        )

        return pd.DataFrame()


# ============================================================
# Cache
# ============================================================

def load_cache():

    try:

        response = cache_table.scan()

        items = response.get(
            "Items",
            []
        )

        return {
            item["favorite_book"]:
                item.get(
                    "recommendations",
                    []
                )
            for item in items
        }

    except Exception as e:

        print(
            f"Failed to load cache: {e}"
        )

        return {}
