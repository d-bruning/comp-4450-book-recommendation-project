import os
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).parent

environment = os.getenv(
    "ENVIRONMENT",
    "development" # development or production
)

config_file = (
    CONFIG_DIR
    / f"{environment}.yml"
)

with open(
    config_file,
    "r",
    encoding="utf-8"
) as f:

    config = yaml.safe_load(f)
