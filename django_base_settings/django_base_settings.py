import sys

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseModel(_BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field_name: field_name.upper(), frozen=True
    )


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        alias_generator=lambda field_name: field_name.upper(), frozen=True
    )


class DjangoBaseSettings(BaseSettings):
    """
    Base class for Django application settings that allows values to be
    overridden by environment variables.

    ### Usage

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

    Field names in `DjangoBaseSettings` are case-insensitive and can be
    overridden through environment variables.
    """

    def __init__(self) -> None:
        super().__init__()
        # Get the module where this instance was created
        module = sys.modules[self.__class__.__module__]
        # Inject validated fields as module-level variables
        self._inject_settings(module, self)

    def _inject_settings(self, module, settings: BaseSettings) -> None:
        for field_name, field_value in settings.model_dump(by_alias=True).items():
            # For nested models, inject a dictionary representation
            if isinstance(
                field_value, (BaseSettings, BaseModel, _BaseSettings, _BaseModel)
            ):
                setattr(
                    module,
                    field_name,
                    field_value.model_dump(by_alias=True),
                )
            else:
                # For regular fields, inject the value directly
                setattr(module, field_name, field_value)
