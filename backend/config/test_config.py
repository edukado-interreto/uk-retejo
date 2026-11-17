"""Storage, context processors, error tracking, URLs and WSGI of the project."""

import importlib
import logging
import logging.config

import pytest
from django.urls import clear_url_caches
from wagtail.models import Site
from wagtailmenus.models import FlatMenu

from config import context_processors, error_tracking
from config.logs import PROD_LOGGING
from config.storage import StaticFilesStorage, vite_prefix


class TestStaticFilesStorage:
    @pytest.fixture
    def storage(self, tmp_path):
        (tmp_path / "uk.css").write_text("body {}")
        storage = StaticFilesStorage(location=tmp_path, base_url="/static/")
        storage.hashed_files = {"uk.css": "uk.abc123.css"}
        return storage

    def test_vite_prefix(self):
        assert vite_prefix() == "vue/"

    def test_hashed_name(self, storage):
        assert storage.stored_name("uk.css") == "uk.abc123.css"

    def test_vite_files_keep_their_name(self, storage):
        # Already hashed by Vite, with their own manifest
        assert (
            storage.stored_name("vue/assets/main-x1y2.js") == "vue/assets/main-x1y2.js"
        )

    def test_missing_file_logs_instead_of_raising(self, storage, caplog):
        with caplog.at_level(logging.WARNING, logger="config.storage"):
            assert storage.stored_name("missing.css") == "missing.css"
        assert "Static file not found: missing.css" in caplog.text

    def test_post_process_skips_vite_files(self, storage, monkeypatch):
        seen = {}

        def post_process(self, paths, dry_run=False, **options):
            seen.update(paths)
            yield from ()

        parent = StaticFilesStorage.__mro__[1]
        monkeypatch.setattr(parent, "post_process", post_process)
        paths = {"uk.css": (storage, "uk.css"), "vue/main.js": (storage, "vue/main.js")}
        assert list(storage.post_process(paths)) == []
        assert seen.keys() == {"uk.css"}


@pytest.mark.django_db
def test_context_processor(rf, settings):
    settings.GOATCOUNTER_URL = "https://uk.goatcounter.com"
    site = Site.objects.get(is_default_site=True)
    for handle in ["piedo", "kapo"]:
        FlatMenu.objects.create(site=site, handle=handle, title=handle)

    request = rf.get("/", HTTP_HOST=site.hostname)
    context = context_processors.app(request)
    assert context["flat_menus"] == ["kapo", "piedo"]
    assert context["ENVIRONMENT"] == settings.ENVIRONMENT
    assert context["GOATCOUNTER_URL"] == "https://uk.goatcounter.com"


def test_setup_bugsink(monkeypatch):
    import sentry_sdk

    calls = {}
    monkeypatch.setattr(sentry_sdk, "init", lambda **kwargs: calls.update(kwargs))

    class Config:
        BUGSINK_DSN = "https://key@bugs.example.org/1"
        COMMIT_HASH = "847a91d"
        HOSTNAME = "uk.example.org"
        ENVIRONMENT = "staging"

    error_tracking.setup_bugsink(Config)
    assert calls["dsn"] == Config.BUGSINK_DSN
    assert calls["release"] == "847a91d"
    assert calls["traces_sample_rate"] == 0


def test_prod_logging_is_valid():
    logging.config.dictConfig({**PROD_LOGGING, "disable_existing_loggers": False})


@pytest.fixture
def reload_urls(settings):
    """Reload config.urls with other settings, then restore the original one."""
    import config.urls

    def reload():
        clear_url_caches()
        return importlib.reload(config.urls)

    yield reload
    settings.DEBUG = False
    reload()


def test_debug_urls_off(reload_urls):
    assert reload_urls().debug_urlpatterns() == []


@pytest.mark.django_db
def test_debug_urls(client, settings, reload_urls, fake_debug_toolbar):
    settings.DEBUG = True
    urls = reload_urls()
    assert urls.debug_urlpatterns()

    response = client.get("/evente")
    assert response.status_code == 302
    assert response.url == "/evente/index.html"
    # The fake registration API of apps.devel
    assert client.get("/api/2027/loaddata").status_code == 200


def test_wsgi_application():
    from config import wsgi

    assert callable(wsgi.application)
