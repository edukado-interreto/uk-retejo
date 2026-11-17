import sys
from datetime import timedelta
from types import ModuleType

import pytest
from django.utils.timezone import now
from wagtail.models import APIToken, Page, Site

from apps.core.models import HomePage, SimplePage
from evente.models import Event, EventeSiteRoot


@pytest.fixture(autouse=True)
def media_root(settings, tmp_path):
    """Uploads and renditions go to a temporary directory, never to ../assets."""
    settings.MEDIA_ROOT = tmp_path


@pytest.fixture
def api_token(django_user_model):
    user = django_user_model.objects.create_user(username="test")
    _obj, plaintext = APIToken.create_token(user=user, name="test")
    return plaintext


@pytest.fixture
def event(db):
    start = now() + timedelta(days=30)
    return Event.objects.create(
        name="Universala Kongreso",
        time_zone="Europe/Bratislava",
        start_date=start,
        end_date=start + timedelta(days=7),
    )


@pytest.fixture
def site_root(db) -> EventeSiteRoot:
    """The page tree of the site: Root > EventeSiteRoot, served by the default site."""
    root = Page.get_first_root_node()
    site_root = root.add_child(instance=EventeSiteRoot(title="UK", slug="uk-root"))
    Site.objects.filter(is_default_site=True).update(root_page=site_root)
    return site_root


@pytest.fixture
def home_page(site_root, event) -> HomePage:
    return site_root.add_child(
        instance=HomePage(title="UK 2027", slug="2027", event=event)
    )


@pytest.fixture
def simple_page(home_page) -> SimplePage:
    return home_page.add_child(instance=SimplePage(title="Aliĝilo", slug="aligxilo"))


@pytest.fixture
def fake_debug_toolbar(monkeypatch):
    """debug_toolbar is left out of INSTALLED_APPS in tests, its modules can't load."""
    toolbar = ModuleType("debug_toolbar.toolbar")
    toolbar.debug_toolbar_urls = list  # type: ignore[attr-defined]
    middleware = ModuleType("debug_toolbar.middleware")
    middleware.show_toolbar = lambda request: True  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "debug_toolbar.toolbar", toolbar)
    monkeypatch.setitem(sys.modules, "debug_toolbar.middleware", middleware)
