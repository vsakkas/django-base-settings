import pytest
from pydantic import ValidationError

from tests.conftest import NestedSettings, SimpleSettings


def test_simple_settings(simple_settings: SimpleSettings) -> None:
    assert simple_settings.allowed_hosts == ["www.example.com"]
    assert simple_settings.debug is False
    assert simple_settings.default_from_email == "webmaster@example.com"


def test_nested_settings(nested_settings: NestedSettings) -> None:
    assert (
        nested_settings.caches["default"].backend
        == "django.core.cache.backends.redis.RedisCache"
    )
    assert nested_settings.caches["default"].location == "redis://127.0.0.1:6379/1"


def test_frozen_simple_settings(simple_settings: SimpleSettings) -> None:
    with pytest.raises(ValidationError):
        simple_settings.allowed_hosts = ["newhost.com"]


def test_frozen_nested_settings(nested_settings: NestedSettings) -> None:
    with pytest.raises(ValidationError):
        nested_settings.caches["default"].location = "redis://localhost:6379/1"
