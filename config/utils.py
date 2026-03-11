import os
import socket
import sys
from enum import Enum
from functools import partial
from typing import cast

from dj_database_url import parse as db_url_parse

parse_db_url = partial(db_url_parse, conn_max_age=600, conn_health_checks=True)


class Environment(Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEV = "dev"
    BUILD = "build"
    TESTING = "testing"

    def __str__(self):
        return self.value

    def display_name(self):
        if self == self.PRODUCTION:
            return ""
        if self == self.STAGING:
            return "TEST"
        return str(self).upper()

    @property
    def deployed(self) -> bool:
        return self in {self.PRODUCTION, self.STAGING}

    @classmethod
    def init(cls, config, debug: bool) -> Environment:
        if is_testing():
            return cls.TESTING
        if debug:
            return cls.DEV
        return cls(config("ENVIRONMENT", "production"))


def is_testing():
    return "test" in sys.argv or "PYTEST_VERSION" in os.environ


def django_vite_dev_mode(debug: bool) -> bool:
    """Checks if `vite` is running the Docker service.

    Always return False in production
    """
    SERVICE_NAME = "vue"

    if not debug:
        return False

    try:
        return bool(socket.gethostbyname(SERVICE_NAME))
    except socket.gaierror:
        return False


def field_panels(*fields: str):
    from wagtail.admin.panels import FieldPanel
    from wagtail.models import Page, PanelPlaceholder

    panels = cast(list[PanelPlaceholder], [FieldPanel(field) for field in fields])
    return Page.content_panels + panels
