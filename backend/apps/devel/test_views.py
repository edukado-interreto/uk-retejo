"""The fake registration API used by uk-aligxilo in development (api/2027/)."""

from datetime import date, timedelta
from http import HTTPStatus

import pytest
from django.urls import URLPattern

from apps.devel import urls
from apps.devel.constants import AGE_GROUPS, COUNTRIES

# The middlewares (redirects, current event) query the database
pytestmark = [pytest.mark.urls("apps.devel.urls"), pytest.mark.django_db]

NOT_IMPLEMENTED = [
    p.pattern._route
    for p in urls.urlpatterns
    if isinstance(p, URLPattern) and p.callback.__name__ not in {
        "checkcode", "loaddata", "get_registration", "participants"
    }
]  # fmt: skip


def this_congress() -> int:
    return (date.today() + timedelta(days=122)).year


@pytest.mark.django_db(False)
def test_not_implemented_helper():
    with pytest.raises(NotImplementedError):
        urls.not_implemented(None)


@pytest.mark.parametrize("route", NOT_IMPLEMENTED)
def test_not_implemented_endpoints(client, route):
    response = client.post(f"/{route}")
    assert response.status_code == HTTPStatus.NOT_IMPLEMENTED
    assert response.json() == {"error": "not implemented"}


def test_checkcode_needs_post(client):
    assert client.get("/checkcode").json() == {"success": False}


@pytest.mark.parametrize("payload", [{}, {"code": ""}, {"code": "abcd-x"}])
def test_checkcode_invalid(client, payload):
    response = client.post("/checkcode", payload, "application/json")
    assert response.json() == {"valid": False}


def test_checkcode_valid(client):
    data = client.post("/checkcode", {"code": "abcdef"}, "application/json").json()
    assert data["valid"] is True
    member = data["member"]
    assert member["ageGroup"] in AGE_GROUPS
    assert member["countryCategory"] in "ABCD"
    assert 1 <= member["countryMembershipCategory"] <= 4


@pytest.mark.parametrize(
    "route, key", [("/loaddata", "allFields"), ("/getRegistration", "registration")]
)
def test_static_payloads(client, route, key):
    response = client.get(route)
    assert response.status_code == 200
    assert key in response.json()


def test_participants_needs_post(client):
    assert client.get("/participants").json() == {"success": False}


@pytest.mark.parametrize("body", [b"", b'{"year": 1887}'])
def test_participants_of_another_year(client, body):
    response = client.post("/participants", body, "application/json")
    assert response.json() == {"valid": False}


def test_participants(client):
    response = client.post(
        "/participants", {"year": this_congress()}, "application/json"
    )
    data = response.json()
    assert data["success"] is True
    assert len(data["participants"]) == 800
    participant = data["participants"][0]
    assert participant.keys() == {"country", "hidden", "first_name", "last_name"}
    assert participant["country"] in COUNTRIES
