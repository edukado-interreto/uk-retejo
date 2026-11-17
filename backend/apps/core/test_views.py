import pytest
from django.urls import resolve, reverse
from wagtail.embeds.exceptions import EmbedNotFoundException
from wagtail.embeds.models import Embed

from apps.core import views
from apps.core.apps import CoreAppConfig

pytestmark = pytest.mark.django_db


def test_favicon_redirects_to_static_file(client):
    response = client.get("/favicon.ico")
    assert response.status_code == 301
    assert response.url.endswith("favicon.ico")


def test_uploads_route(settings):
    match = resolve(f"{settings.MEDIA_URL}docs/plan.txt")
    assert match.func is views.serve_upload
    assert match.kwargs["path"] == "docs/plan.txt"
    assert "document_root" in match.kwargs


def test_uploads_are_served_with_cache_header(rf, tmp_path):
    (tmp_path / "plan.txt").write_text("UK")
    response = views.serve_upload(rf.get("/"), "plan.txt", document_root=tmp_path)
    assert response.headers["Cache-Control"] == "max-age=7776000, public"
    assert b"".join(response.streaming_content) == b"UK"


def test_missing_upload_is_404(client, settings):
    assert client.get(f"{settings.MEDIA_URL}missing.pdf").status_code == 404


def test_get_embed_without_url(client):
    response = client.get("/wagtail/api/html/get-embed")
    assert response.status_code == 400
    assert response.json() == {"error": "No field 'url' found in body"}


def test_get_embed_unknown_url(client, monkeypatch):
    def not_found(url):
        raise EmbedNotFoundException

    monkeypatch.setattr(views, "get_embed", not_found)
    response = client.get("/wagtail/api/html/get-embed", {"url": "https://example.org"})
    assert response.status_code == 400


def test_get_embed_returns_html(client, monkeypatch):
    embed = Embed(url="https://example.org", html="<iframe></iframe>")
    monkeypatch.setattr(views, "get_embed", lambda url: embed)
    response = client.get("/wagtail/api/html/get-embed", {"url": "https://example.org"})
    assert response.status_code == 200
    assert response.content == b"<iframe></iframe>"


@pytest.mark.parametrize("setting", ["DJANGO_ADMIN_URL", "WAGTAIL_ADMIN_URL"])
def test_admin_urls_without_slash_redirect(client, settings, setting):
    prefix = getattr(settings, setting)
    response = client.get(f"/{prefix}")
    assert response.status_code == 302
    assert response.url == f"/{prefix}/"


def test_django_admin_lists_embeds(admin_client):
    url = reverse("admin:wagtailembeds_embed_changelist")
    assert admin_client.get(url).status_code == 200


@pytest.mark.parametrize("url", ["/404", "/404/abc"])
def test_404_page(client, url):
    assert client.get(url).status_code == 404


def test_500_page(client):
    assert client.get("/500").status_code == 500


class TestMcpConnectionPatch:
    """CoreAppConfig.ready() closes DB connections after each MCP tool call."""

    @pytest.fixture
    def dispatch(self):
        return pytest.importorskip("wagtail_mcp.dispatch")

    def test_without_wagtail_mcp(self, monkeypatch):
        from django.apps import apps

        monkeypatch.setattr(apps, "is_installed", lambda name: False)
        CoreAppConfig.ready(None)  # Nothing to patch, nothing raised

    def test_patch_closes_connections(self, dispatch, monkeypatch):
        from django.apps import apps
        from django.db import connections

        calls = []
        monkeypatch.setattr(apps, "is_installed", lambda name: True)
        monkeypatch.setattr(
            dispatch.DjangoClient, "request", lambda self, *a, **kw: "response"
        )
        monkeypatch.setattr(connections, "close_all", lambda: calls.append("closed"))

        CoreAppConfig.ready(None)
        patched = dispatch.DjangoClient.request
        assert patched._closes_connections

        # Idempotent: a second call keeps the same wrapper
        CoreAppConfig.ready(None)
        assert dispatch.DjangoClient.request is patched

        assert patched(None) == "response"
        assert calls == ["closed"]
