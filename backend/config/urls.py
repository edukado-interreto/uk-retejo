import re

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import urlpatterns as static_urlpatterns
from django.http import Http404
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from pattern_library import urls as pattern_library_urls
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.admin.auth import require_admin_access
from wagtail.api.v3.urls import api as api_v3
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.utils.urlpatterns import decorate_urlpatterns

from apps.core import views as core_views
from apps.search import views as search_views
from evente import urls as evente_urls
from evente.views import page_not_found, server_error

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    from apps.devel import urls as dev_urls


def debug_urlpatterns():
    if settings.DEBUG:
        return [
            *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
            # API for testing:
            path("api/2027/", include(dev_urls)),
            # Evente by Themeadapt
            path("evente", RedirectView.as_view(url="/evente/index.html")),
            path("evente/", include(evente_urls)),
            *debug_toolbar_urls(),
        ]
    return []


def admin_redirect(prefix):
    return [path(prefix, RedirectView.as_view(url=f"/{prefix}/", permanent=False))]


urlpatterns = [
    path("favicon.ico", core_views.favicon),
    *static_urlpatterns,
    # Uploads are served by Django, also in production
    re_path(
        rf"^{re.escape(settings.MEDIA_URL.lstrip('/'))}(?P<path>.*)$",
        core_views.serve_upload,
        {"document_root": settings.MEDIA_ROOT},
    ),
    path("wagtail/api/html/get-embed", core_views.api_get_embed),
    # Both admins need a trailing slash, as APPEND_SLASH is False
    *admin_redirect(settings.DJANGO_ADMIN_URL),
    path(f"{settings.DJANGO_ADMIN_URL}/", admin.site.urls),
    path(
        f"{settings.WAGTAIL_ADMIN_URL}/patterns/",
        include(
            (
                decorate_urlpatterns(
                    pattern_library_urls.urlpatterns, require_admin_access
                ),
                pattern_library_urls.app_name,
            )
        ),
    ),
    *admin_redirect(settings.WAGTAIL_ADMIN_URL),
    path(f"{settings.WAGTAIL_ADMIN_URL}/", include(wagtailadmin_urls)),
    path("dokumentoj/", include(wagtaildocs_urls)),
    path("trovi", search_views.search, name="search"),
    *debug_urlpatterns(),
    re_path("404/?.*", page_not_found, {"exception": Http404("Page not found")}),
    path("500", server_error),
    path("api/v3/", api_v3.urls),
    path("mcp", include("wagtail_mcp.urls")),
    path("", include(wagtail_urls)),
]

handler404 = "evente.views.page_not_found"
handler500 = "evente.views.server_error"
