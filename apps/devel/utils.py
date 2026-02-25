from datetime import date, timedelta
from random import choices, randint

from faker import Faker
from slugify.slugify import slugify

from apps.devel.constants import (
    AGE_GROUP_WEIGHTS,
    AGE_GROUPS,
    COUNTRIES,
    COUNTRY_WEIGHTS,
    LOCALES_BY_COUNTRY,
    MISSING_FIELDS,
)

__all__ = [
    "current_year",
    "get_faker",
    "mostly",
    "random_age_group",
    "random_country",
    "random_missing_fields",
    "random_names",
    "to_latin",
]


def weight_choice(collection, weights):
    return choices(collection, weights, k=1)[0]


def current_year(year, today=date.today()) -> int:
    # Ni diru ke turndato estas 1-a de septembro, ~122 tagoj ĝis fino de jaro
    remainder = timedelta(365 - (date(1905, 9, 1) - date(1905, 1, 1)).days)
    try:
        year = int(year)
    except ValueError:
        return False
    return year == (today + remainder).year


def random_missing_fields() -> list[str]:
    return choices(MISSING_FIELDS, k=randint(1, len(MISSING_FIELDS)))


def random_age_group() -> str | None:
    return weight_choice(AGE_GROUPS, AGE_GROUP_WEIGHTS)


def random_country() -> str:
    return weight_choice(COUNTRIES, COUNTRY_WEIGHTS)


def get_faker(country_code: str, default="pl_PL") -> Faker:
    return Faker(LOCALES_BY_COUNTRY.get(country_code, [default]))


def random_names(fake: Faker):
    try:
        return fake.first_romanized_name(), fake.last_romanized_name()
    except AttributeError:
        return fake.first_name(), fake.last_name()


def mostly(mostly: bool = True) -> bool:
    return choices([mostly, not mostly], weights=[98, 2])[0]


def is_latin(string: str):
    char = string[0]
    if not isinstance(char, str) or len(char) != 1:
        raise ValueError("Input must be a single character string.")

    codepoint = ord(char)
    return 0x0000 <= codepoint <= 0x024F


def to_latin(name):
    return slugify(
        name, separator=" ", lowercase=False, allow_unicode=is_latin(name)
    ).title()
