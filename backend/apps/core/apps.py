from django.apps import AppConfig
from wagtail.images.apps import WagtailImagesAppConfig


class CoreAppConfig(AppConfig):
    name = "apps.core"
    # Several AppConfig classes in this module, Django needs to know which one to use
    default = True

    def ready(self):
        """Close the DB connections opened by the MCP tools.

        The MCP SDK runs the tools in worker threads, where Django never closes
        the connections (the test Client used by wagtail_mcp disconnects
        close_old_connections). They stay idle in Postgres until garbage collected.
        """
        from django.apps import apps
        from django.db import connections

        if not apps.is_installed("wagtail_mcp"):
            return
        from wagtail_mcp import dispatch

        if getattr(dispatch.DjangoClient.request, "_closes_connections", False):
            return

        original_request = dispatch.DjangoClient.request

        def request_and_close(self, *args, **kwargs):
            try:
                return original_request(self, *args, **kwargs)
            finally:
                connections.close_all()

        request_and_close._closes_connections = True
        dispatch.DjangoClient.request = request_and_close


class CustomImagesAppConfig(WagtailImagesAppConfig):
    default_attrs = {"decoding": "async", "loading": "lazy"}
