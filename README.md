# Django Base Settings

[![Python](https://img.shields.io/badge/python-3.10+-187f58.svg)](https://www.python.org/downloads/)
![Django Version](https://img.shields.io/badge/django-5.0+-187f58)
[![MIT License](https://img.shields.io/badge/license-MIT-187f58)](https://github.com/vsakkas/django-base-settings/blob/master/LICENSE)

Use Pydantic to enhance your Django application settings.

## Requirements

- Python 3.10 or newer

## Installation

To install Django Base Settings, run the following command:

```bash
poetry add django-base-settings
```

## Usage

In your Django settings file, define a subclass of `DjangoBaseSettings`:

```python
from django_base_settings import DjangoBaseSettings

class MySiteSettings(DjangoBaseSettings):
    allowed_hosts: list[str] = ["www.example.com"]
    debug: bool = False
    default_from_email: str = "webmaster@example.com"

my_site_settings = MySiteSettings()
```

This is equivalent to:

```python
ALLOWED_HOSTS = ["www.example.com"]
DEBUG = False
DEFAULT_FROM_EMAIL = "webmaster@example.com"
```

### Nested Settings

For more complex configurations, you can define nested settings using Pydantic models:

```python
from pydantic import Field
from pydantic_settings import BaseSettings

from django_base_settings import DjangoBaseSettings

class CacheSettings(BaseSettings):
    backend: str = Field("django.core.cache.backends.redis.RedisCache", alias="BACKEND")
    location: str = Field("redis://127.0.0.1:6379/1", alias="LOCATION")

class MySiteSettings(DjangoBaseSettings):
    caches: dict[str, CacheSettings] = {
        "default": CacheSettings()
    }

my_site_settings = MySiteSettings()
```

This configuration is equivalent to:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

### Environment Variables

Fields contained within DjangoBaseSettings and BaseSettings objects can be assigned values or have their default overwritten through environment variables, providing flexibility for different deployment environments.

In this example:

```python
from django_base_settings import DjangoBaseSettings

class MySiteSettings(DjangoBaseSettings):
    default_from_email: str = "webmaster@example.com"

my_site_settings = MySiteSettings()
```

You can configure the value of default_from_email by creating an environment variable, which will overwrite the default value:

```bash
export DEFAULT_FROM_EMAIL="admin@example.com"
```

You can also specify a different environment variable name:

```python
from pydantic import Field

from django_base_settings import DjangoBaseSettings

class MySiteSettings(DjangoBaseSettings):
    default_from_email: str = Field("webmaster@example.com", env="DEFAULT_EMAIL")

my_site_settings = MySiteSettings()
```

In this example, setting `DEFAULT_EMAIL` as an environment variable will override the default value of `default_from_email`.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/vsakkas/django-base-settings/blob/master/LICENSE) file for details.
