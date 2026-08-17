from src.config.loader import config

provider = (
    config["storage"]["provider"]
)

if provider == "dynamodb":

    from src.api.storage.dynamodb_storage import (
        save_feedback
    )

else:

    from src.api.storage.local_storage import (
        save_feedback
    )
