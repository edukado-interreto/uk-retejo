import socket
import sys

import pytest

from config import utils
from config.utils import Environment


@pytest.mark.parametrize(
    "env, name, deployed",
    [
        (Environment.PRODUCTION, "", True),
        (Environment.STAGING, "TEST", True),
        (Environment.DEV, "DEV", False),
        (Environment.BUILD, "BUILD", False),
        (Environment.TESTING, "TESTING", False),
    ],
)
def test_environment(env, name, deployed):
    assert env.display_name() == name
    assert env.deployed is deployed
    assert str(env) == env.value


def test_environment_is_attributes():
    assert Environment.STAGING.is_staging is True
    assert Environment.STAGING.is_production is False
    with pytest.raises(AttributeError):
        _ = Environment.STAGING.is_unknown


def test_environment_init_in_tests():
    assert Environment.init(lambda *args: "production", debug=False).is_testing


@pytest.mark.parametrize(
    "debug, env_value, expected",
    [(True, "production", Environment.DEV), (False, "staging", Environment.STAGING)],
)
def test_environment_init(monkeypatch, debug, env_value, expected):
    monkeypatch.setattr(utils, "is_testing", lambda: False)
    assert Environment.init(lambda name, default: env_value, debug) is expected


def test_environment_init_defaults_to_production(monkeypatch):
    monkeypatch.setattr(utils, "is_testing", lambda: False)
    assert Environment.init(lambda name, default: default, False).is_production


def test_is_testing(monkeypatch):
    assert utils.is_testing()
    monkeypatch.delenv("PYTEST_VERSION")
    monkeypatch.setattr(sys, "argv", ["manage.py", "test"])
    assert utils.is_testing()
    monkeypatch.setattr(sys, "argv", ["manage.py", "runserver"])
    assert not utils.is_testing()


def unknown_host(name):
    raise socket.gaierror


def test_vite_dev_mode_off_without_debug():
    assert utils.django_vite_dev_mode(False) is False


@pytest.mark.parametrize(
    "resolve, expected", [(unknown_host, False), (lambda n: "10.0.0.5", True)]
)
def test_vite_dev_mode_with_vue_service(monkeypatch, resolve, expected):
    monkeypatch.setattr(socket, "gethostbyname", resolve)
    assert utils.django_vite_dev_mode(True) is expected


def test_field_panels():
    from wagtail.models import Page

    panels = utils.field_panels("body", "hero")
    assert panels[: len(Page.content_panels)] == Page.content_panels
    assert [p.field_name for p in panels[len(Page.content_panels) :]] == [
        "body",
        "hero",
    ]


def test_internal_ips(monkeypatch):
    monkeypatch.setattr(socket, "gethostbyname", lambda name: "172.18.0.5")
    ips = utils.InternalIPs()
    assert "172.18.0.1" in ips
    assert "172.18.1.1" not in ips
    assert len(list(ips)) == 256


@pytest.mark.parametrize(
    "path, query, headers, shown",
    [
        ("/admin/pages/", "", {"HTTP_ACCEPT": "*/*"}, False),
        ("/2027/", "in_preview_panel=1", {"HTTP_ACCEPT": "*/*"}, False),
        ("/2027/", "", {}, False),  # Real Wagtail preview requests
        ("/wagtail/patterns/", "", {"HTTP_ACCEPT": "*/*"}, False),
        ("/2027/", "", {"HTTP_ACCEPT": "*/*"}, True),
    ],
)
def test_show_toolbar_on_wagtail(rf, fake_debug_toolbar, path, query, headers, shown):
    request = rf.get(f"{path}?{query}", **headers)
    assert utils.show_toolbar_on_wagtail(request) is shown
