# Export every configuration from this file. Do no get environment variables at runtime

import os
from typing import Optional

import toml

project = toml.load(os.path.join(os.path.dirname(__file__), "../pyproject.toml"))
poetry = project.get("tool", {}).get("poetry", {})

APP_TITLE: str = poetry.get("name", "")
APP_DESCRIPTION: str = poetry.get("description", "")
APP_VERSION: str = poetry.get("version", "")
