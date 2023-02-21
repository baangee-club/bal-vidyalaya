from pydantic import BaseSettings
from functools import lru_cache
from typing import Any


class Settings(BaseSettings):
    atlas_uri: str
    db_name: str
    access_token_expire_minutes: int
    algorithm: str
    secret_key: str
    username: bytes
    password: bytes
    log_level: str


@lru_cache()
def get_settings():
    return Settings()
