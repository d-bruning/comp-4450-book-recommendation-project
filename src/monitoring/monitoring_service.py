from src.config.loader import config

provider = (
    config["storage"]["provider"]
)

if provider == "dynamodb":

    from src.monitoring.storage.dynamodb_monitoring_storage import (
        load_cache,
        load_feedback,
        load_prediction_logs
    )

else:

    from src.monitoring.storage.local_monitoring_storage import (
        load_cache,
        load_feedback,
        load_prediction_logs
    )
