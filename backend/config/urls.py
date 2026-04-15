from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import urlpatterns as static_urlpatterns
from django.contrib.staticfiles.views import serve
from django.core.files.storage import storages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django_rsgi.urls import media_urlpatterns
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from apps.base.views import serve_upload
from apps.search import views as search_views
from evente import urls as evente_urls

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    from apps.devel import urls as dev_urls


@cache_page(60 * 60 * 24 * 30)
def favicon(_request: HttpRequest):
    return redirect(storages["staticfiles"].url("favicon.ico"), permanent=True)


def debug_urlpatterns():
    if settings.DEBUG:
        return [
            *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
            # API for testing:
            path("api/2026/", include(dev_urls)),
            # Evente by Themeadapt
            path("evente/", include(evente_urls)),
            *debug_toolbar_urls(),
        ]
    return []


urlpatterns = [
    path("favicon.ico", favicon),
    *static_urlpatterns,
    *media_urlpatterns(view=serve_upload),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    *debug_urlpatterns(),
    path("", include(wagtail_urls)),
]
