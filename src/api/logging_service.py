from src.config.loader import config

provider = (
    config["storage"]["provider"]
)

if provider == "dynamodb":

    from src.api.storage.dynamodb_storage import (
        log_prediction
    )

else:

    from src.api.storage.local_storage import (
        log_prediction
    )
