from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.http import HttpRequest, HttpResponse

from whitenoise.responders import StaticFile
from whitenoise.middleware import WhiteNoiseMiddleware
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from apps.search import views as search_views
from config.settings import CONFIG_DIR


def favicon(request: HttpRequest):
    static_file = StaticFile(
        path=CONFIG_DIR / "static" / "favicon.ico",
        headers=[("Content-Type", "image/x-icon")],
    )
    return WhiteNoiseMiddleware.serve(static_file, request)


urlpatterns = [
    path("favicon.ico", favicon),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
