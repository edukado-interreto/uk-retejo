from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import urlpatterns as static_urlpatterns
from django.urls import include, path
from django_rsgi.urls import media_urlpatterns
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from apps.base.views import serve_upload
from apps.core import views as core_views
from apps.search import views as search_views
from evente import urls as evente_urls
from evente.views import error_404, error_500

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
            path("evente/", include(evente_urls)),
            *debug_toolbar_urls(),
        ]
    return []


urlpatterns = [
    path("favicon.ico", core_views.favicon),
    *static_urlpatterns,
    *media_urlpatterns(view=serve_upload),
    path("wagtail/api/html/get-embed/", core_views.api_get_embed),
    path(f"{settings.DJANGO_ADMIN_URL}/", admin.site.urls),
    path(f"{settings.WAGTAIL_ADMIN_URL}/", include(wagtailadmin_urls)),
    path("dokumentoj/", include(wagtaildocs_urls)),
    path("trovi/", search_views.search, name="search"),
    *debug_urlpatterns(),
    path("404/", error_404),
    path("500/", error_500),
    path("", include(wagtail_urls)),
]
