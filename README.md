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

Field names in `DjangoBaseSettings` are case-insensitive and can be overridden through environment variables.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/vsakkas/django-base-settings/blob/master/LICENSE) file for details.
