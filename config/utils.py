import socket
from functools import partial
from typing import cast

from dj_database_url import parse as db_url_parse

parse_db_url = partial(db_url_parse, conn_max_age=600, conn_health_checks=True)


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
