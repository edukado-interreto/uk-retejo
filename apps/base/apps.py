from django.apps import AppConfig
from wagtail.images.apps import WagtailImagesAppConfig


class BaseAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.base"


class CustomImagesAppConfig(WagtailImagesAppConfig):
    default_attrs = {"decoding": "async", "loading": "lazy"}
