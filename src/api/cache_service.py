from src.api.config import USE_DYNAMODB

if USE_DYNAMODB:

    from src.api.storage.dynamodb_storage import (
        get_cached_prediction,
        cache_prediction
    )

else:

    from src.api.storage.local_storage import (
        get_cached_prediction,
        cache_prediction
    )
