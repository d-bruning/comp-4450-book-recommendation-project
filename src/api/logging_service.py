from src.api.config import USE_DYNAMODB

if USE_DYNAMODB:
    from src.api.storage.dynamodb_storage import (
        log_prediction
    )
else:
    from src.api.storage.local_storage import (
        log_prediction
    )
