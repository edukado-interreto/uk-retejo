from django.conf import settings
from django.contrib import admin
from django.core.files.storage import storages
from django.shortcuts import redirect
from django.urls import include, path
from django.views.decorators.cache import cache_page

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.models.pages import HttpRequest

from apps.search import views as search_views
from config.dev import urls as dev_urls


@cache_page(60 * 60 * 24 * 30)
def favicon(_request: HttpRequest):
    return redirect(storages["staticfiles"].url("favicon.ico"), permanent=True)


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

    # API for testing
    urlpatterns += [path("api/2025/", include(dev_urls))]

urlpatterns += [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
