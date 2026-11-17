import pytest
from django.core.management import call_command
from django.urls import reverse

from apps.core.models import SimplePage

pytestmark = pytest.mark.django_db


@pytest.fixture
def many_pages(home_page):
    for i in range(12):
        home_page.add_child(
            instance=SimplePage(title=f"Ekskurso {i}", slug=f"ekskurso-{i}")
        )
    call_command("update_index", verbosity=0)


def test_search_without_query(client):
    response = client.get(reverse("search"))
    assert response.status_code == 200
    assert response.context["search_query"] is None
    assert len(response.context["search_results"]) == 0


def test_search_finds_live_pages(client, many_pages):
    response = client.get(reverse("search"), {"query": "Ekskurso"})
    results = response.context["search_results"]
    assert results.paginator.count == 12
    assert len(results) == 10
    assert results.has_next()


@pytest.mark.parametrize("page, number", [("2", 2), ("abc", 1), ("99", 2)])
def test_search_pagination(client, many_pages, page, number):
    response = client.get(reverse("search"), {"query": "Ekskurso", "page": page})
    assert response.context["search_results"].number == number


def test_search_without_results(client, home_page):
    response = client.get(reverse("search"), {"query": "neniu"})
    assert response.status_code == 200
    assert response.context["search_results"].paginator.count == 0
