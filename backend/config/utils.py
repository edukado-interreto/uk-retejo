import os
import socket
import sys
from enum import Enum
from ipaddress import ip_address, ip_network
from typing import cast

from django.http import HttpRequest
from django.utils.module_loading import import_string


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
    def init(cls, env, debug: bool) -> Environment:
        if is_testing():
            return cls.TESTING
        if debug:
            return cls.DEV
        return cls(env("ENVIRONMENT", "production"))

    def __getattr__(self, attr) -> bool:
        """Check the enum’s value by attribute

        >>> ENVIRONMENT = Environment.DEV
        >>> ENVIRONMENT.is_dev
        True
        >>> ENVIRONMENT.is_production
        False
        """
        name = attr.replace("is_", "")
        if name in (e.value for e in type(self)):
            return self.value == name
        return super().__getattribute__(name)


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


class InternalIPs:
    def __init__(self):
        hostname = "django"
        ip = socket.gethostbyname(hostname)
        self.network = ip_network(f"{ip}/24", strict=False)

    def __iter__(self):
        return (str(addr) for addr in self.network)

    def __contains__(self, address):
        return ip_address(address) in self.network


def show_toolbar_on_wagtail(request) -> bool:
    """
    Determine whether to show the toolbar on a given page in Wagtail.
    """
    in_wagtail_admin = "/admin/" in request.path
    is_preview_request = "in_preview_panel" in request.GET
    # Real preview request has very few headers:
    is_admin_preview = "HTTP_ACCEPT" not in request.META

    if any([in_wagtail_admin, is_preview_request, is_admin_preview]):
        return False
    return import_string("debug_toolbar.middleware.show_toolbar")(request)
