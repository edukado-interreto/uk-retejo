import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from apps.core.models import HomePage, SimplePage

pytestmark = pytest.mark.django_db

UNIQUE_ID = "0123456789abcdef0123456789abcdef"


def test_home_page_only_under_site_root():
    assert HomePage.parent_page_types == ["evente.EventeSiteRoot"]


def test_home_page_renders(client, home_page):
    response = client.get(home_page.url)
    assert response.status_code == 200
    assert "core/home_page.html" in [t.name for t in response.templates]
    soup = BeautifulSoup(response.content, "html.parser")
    assert "homepage" in soup.body["class"]


def test_project_blocks_render_in_evente_sections(client, home_page):
    """The blocks of content_blocks.py are registered in the sections of evente."""
    timeline = [{"type": "events", "value": {"date": "2027-08-01"}}]
    raw = [
        {
            "type": "section",
            "value": {"content": [{"type": "timeline", "value": timeline}]},
        }
    ]
    home_page.body = HomePage.body.field.stream_block.to_python(raw)
    home_page.save()

    soup = BeautifulSoup(client.get(home_page.url).content, "html.parser")
    assert soup.select_one("main ul.timeline li.day") is not None


def test_simple_page_renders(client, simple_page):
    response = client.get(simple_page.url)
    assert response.status_code == 200
    assert response.context["page"] == simple_page
    assert "unique_id" not in response.context


def test_simple_page_mendilo_route(client, simple_page):
    response = client.get(f"{simple_page.url}/{UNIQUE_ID}/")
    assert response.status_code == 200
    assert response.context["unique_id"] == UNIQUE_ID


@pytest.mark.parametrize("unique_id", ["xyz", "0123", f"{UNIQUE_ID}0123456"])
def test_simple_page_mendilo_rejects_invalid_ids(client, simple_page, unique_id):
    assert client.get(f"{simple_page.url}/{unique_id}/").status_code == 404


def test_simple_page_mendilo_view_without_id(rf, simple_page):
    response = SimplePage.mendilo(simple_page, rf.get(simple_page.url))
    assert "unique_id" not in response.context_data


def test_pattern_library_menu_item(admin_client):
    response = admin_client.get(reverse("wagtailadmin_home"))
    assert response.status_code == 200
    assert reverse("pattern_library:index").encode() in response.content


def test_pattern_library_requires_admin_access(client):
    response = client.get(reverse("pattern_library:index"))
    assert response.status_code == 302
    assert reverse("wagtailadmin_login") in response.url


def test_pattern_library_renders_project_patterns(admin_client):
    url = reverse(
        "pattern_library:render_pattern",
        kwargs={"pattern_template_name": "core/blocks/program/timeline_block.html"},
    )
    response = admin_client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert len(soup.select("ul.timeline li.day")) == 3
