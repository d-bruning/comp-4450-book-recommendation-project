import os

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)

USE_DYNAMODB = (
    ENVIRONMENT == "production"
)
