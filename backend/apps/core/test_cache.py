import pytest
from django.core.cache import cache
from wagtail.coreutils import make_wagtail_template_fragment_key
from wagtailmenus.models import FlatMenu

from apps.core.cache import cache_burst
from apps.core.models import SimplePage
from evente.models import EventSettings


def fragment_key(name, page, *vary_on):
    """Key of a fragment cached with vary_on + CACHE_BURST + page and site."""
    vary_on = [*vary_on, cache_burst()]
    return make_wagtail_template_fragment_key(name, page, page.get_site(), vary_on)


def test_cache_burst_is_stable():
    assert cache_burst() == cache_burst()


@pytest.mark.django_db
def test_publishing_a_page_busts_the_cache(home_page):
    before = cache_burst()
    home_page.title = "Nova titolo"
    home_page.save_revision().publish()
    assert cache_burst() != before


@pytest.mark.django_db
def test_moving_a_page_busts_the_cache(home_page, simple_page):
    other = home_page.add_child(instance=SimplePage(title="Alia", slug="alia"))
    before = cache_burst()
    simple_page.move(other, pos="last-child")
    assert cache_burst() != before


@pytest.mark.django_db
def test_menus_and_settings_bust_the_cache(home_page, event):
    before = cache_burst()
    FlatMenu.objects.create(site=home_page.get_site(), handle="piedo", title="Piedo")
    after_menu = cache_burst()
    assert after_menu != before

    event_settings, _ = EventSettings.objects.get_or_create(event=event)
    after_create = cache_burst()
    event_settings.save()
    assert cache_burst() != after_create


@pytest.mark.django_db
def test_unrelated_models_keep_the_cache(django_user_model):
    before = cache_burst()
    django_user_model.objects.create_user(username="vizitanto")
    assert cache_burst() == before


@pytest.mark.django_db
def test_fragments_cached_then_invalidated(client, settings, home_page):
    settings.TEMPLATE_CACHE_TTL = 60
    response = client.get(home_page.url)
    assert response.status_code == 200
    page, lang = response.context["page"], response.context["LANGUAGE_CODE"]
    keys = {
        "header": fragment_key("header", page, lang),
        "footer": fragment_key("footer", page, lang),
        "home": fragment_key("home", page),
    }
    assert all(cache.get(key) is not None for key in keys.values())

    # Saving another page renews CACHE_BURST: the old fragments are never read again
    home_page.add_child(instance=SimplePage(title="Nova", slug="nova"))
    assert fragment_key("header", page, lang) != keys["header"]
