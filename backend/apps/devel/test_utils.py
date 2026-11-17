from datetime import date

import pytest
from faker import Faker

from apps.devel import utils
from apps.devel.constants import (
    AGE_GROUP_WEIGHTS,
    AGE_GROUPS,
    COUNTRIES,
    COUNTRY_WEIGHTS,
    LOCALES_BY_COUNTRY,
    MISSING_FIELDS,
)
from evente.structure.layouts import BodyContent


def test_constants_are_consistent():
    assert len(AGE_GROUPS) == len(AGE_GROUP_WEIGHTS)
    assert len(COUNTRIES) == len(COUNTRY_WEIGHTS)
    # Every country of the participants has names in its language
    assert set(COUNTRIES) <= LOCALES_BY_COUNTRY.keys()


@pytest.mark.parametrize(
    "year, today, expected",
    [
        (2027, date(2027, 8, 31), True),
        # From September, the next congress is the one of next year
        (2027, date(2026, 9, 1), True),
        (2026, date(2026, 9, 1), False),
        ("2027", date(2027, 1, 1), True),
        ("abc", date(2027, 1, 1), False),
    ],
)
def test_current_year(year, today, expected):
    assert utils.current_year(year, today) is expected


def test_current_year_defaults_to_today():
    assert utils.current_year(1887) is False


def test_random_helpers():
    fields = utils.random_missing_fields()
    assert 1 <= len(fields) <= len(MISSING_FIELDS)
    assert set(fields) <= set(MISSING_FIELDS)
    assert utils.random_age_group() in AGE_GROUPS
    assert utils.random_country() in COUNTRIES
    assert utils.mostly(True) in (True, False)


@pytest.mark.parametrize("country, locale", [("FR", "fr_FR"), ("XX", "pl_PL")])
def test_get_faker(country, locale):
    assert utils.get_faker(country).locales == [locale]


def test_random_names_romanized():
    first, last = utils.random_names(Faker("ja_JP"))
    assert first.isascii() and last.isascii()


def test_random_names_fallback():
    first, last = utils.random_names(Faker("fr_FR"))
    assert first and last


@pytest.mark.parametrize(
    "name, expected",
    [
        ("élodie", "Élodie"),
        ("jean-luc", "Jean Luc"),
        ("Дмитрий", "Dmitrii"),
        ("Βασίλης", "Basiles"),
    ],
)
def test_to_latin(name, expected):
    assert utils.to_latin(name) == expected


def test_is_latin_needs_a_character():
    with pytest.raises(ValueError):
        utils.is_latin(["ab"])


@pytest.mark.django_db
@pytest.mark.parametrize("use_specific, by_username", [(True, True), (False, False)])
def test_save_page_publishes_a_revision(
    simple_page, admin_user, use_specific, by_username
):
    raw = [{"type": "section", "value": {"content": []}}]
    page = simple_page if use_specific else simple_page.page_ptr
    user = admin_user.username if by_username else admin_user
    utils.save_page(page, {"body": (BodyContent, raw)}, user=user)

    simple_page.refresh_from_db()
    assert simple_page.live_revision.user == admin_user
    assert [block.block_type for block in simple_page.body] == ["section"]
