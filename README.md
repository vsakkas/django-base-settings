# Django Base Settings

[![Latest Release](https://img.shields.io/github/v/release/vsakkas/django-base-settings.svg?color=187f58)](https://github.com/vsakkas/django-base-settings/releases/tag/v0.5.0)
[![Python](https://img.shields.io/badge/python-3.10+-187f58.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-5.0+-187f58)](https://www.djangoproject.com/)
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
from django_base_settings import BaseSettings, DjangoBaseSettings

class CacheSettings(BaseSettings):
    backend: str = "django.core.cache.backends.redis.RedisCache"
    location: str = "redis://127.0.0.1:6379/1"

class MySiteSettings(DjangoBaseSettings):
    caches: dict[str, CacheSettings] = {"default": CacheSettings()}

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

> [!NOTE]
> Import `BaseModel`/`BaseSettings` from `django_base_settings` for your nested configuration objects instead of `pydantic`/`pydantic_settings`. These provide additional features, which are necessary to generate a valid Django configuration.

### Environment Variables

Fields contained within `DjangoBaseSettings` and `BaseSettings` objects can be a assigned value or have their default value overwritten through environment variables, providing flexibility for different deployment environments.

In this example:

```python
from django_base_settings import DjangoBaseSettings

class MySiteSettings(DjangoBaseSettings):
    default_from_email: str = "webmaster@example.com"

my_site_settings = MySiteSettings()
```

Setting `DEFAULT_FROM_EMAIL` as an environment variable will override the default value of `default_from_email`:

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

In this example, setting `DEFAULT_EMAIL` as an environment variable will override the default value of `default_from_email`:

```bash
export DEFAULT_EMAIL="admin@example.com"
```

### Pydantic Fields

You can use fields from Pydantic to further enhance your settings and improve the validation of the configuration. For example, for setting up `CacheSettings`, you can define the `location` as `RedisDsn` instead of `str`:

```python
from pydantic import RedisDsn

from django_base_settings import BaseSettings, DjangoBaseSettings

class CacheSettings(BaseSettings):
    backend: str = "django.core.cache.backends.redis.RedisCache"
    location: RedisDsn = "redis://127.0.0.1:6379/1"

class MySiteSettings(DjangoBaseSettings):
    caches: dict[str, CacheSettings] = {"default": CacheSettings()}

my_site_settings = MySiteSettings()
```

The above code ensures the`location` field adheres to the `RedisDsn` format, providing an extra layer of validation on your settings.

> [!TIP]
> For more detailed information on DSN types and their usage, refer to the [pydantic](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks) documentation on network types.

### Altering Settings

Django does not recommend altering the application settings during runtime. To align with this best practice, all fields defined using DjangoBaseSettings are immutable and cannot be modified after initialization.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/vsakkas/django-base-settings/blob/master/LICENSE) file for details.
