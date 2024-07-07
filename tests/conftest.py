import pytest

from django_base_settings import BaseSettings, DjangoBaseSettings


# Simple settings
class SimpleSettings(DjangoBaseSettings):
    allowed_hosts: list[str] = ["www.example.com"]
    debug: bool = False
    default_from_email: str = "webmaster@example.com"


# Nested settings
class CacheSettings(BaseSettings):
    backend: str = "django.core.cache.backends.redis.RedisCache"
    location: str = "redis://127.0.0.1:6379/1"


class NestedSettings(DjangoBaseSettings):
    caches: dict[str, CacheSettings] = {"default": CacheSettings()}


@pytest.fixture
def simple_settings() -> SimpleSettings:
    return SimpleSettings()


@pytest.fixture
def nested_settings() -> NestedSettings:
    return NestedSettings()
