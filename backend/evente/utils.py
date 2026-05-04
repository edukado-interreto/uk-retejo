import re
from urllib.parse import urlparse, parse_qs
from collections.abc import Sequence
from typing import overload


@overload
def first[T](iterable: Sequence[T], default: T) -> T: ...


@overload
def first[T](iterable: Sequence[T], default: T | None = None): ...


def first[T](iterable: Sequence[T], default: T | None = None):
    try:
        return iterable[0]
    except IndexError:
        return default


def split_by(blocks, setting_blocks):
    settings = set(setting_blocks)
    return ([b for b in blocks if b not in settings], setting_blocks)


def snake_case(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def uniq(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def parse_osm(value: str):
    """https://osm.org/#map=12/53.1276/23.0534&layers=N"""
    fragment = parse_qs(urlparse(value).fragment)
    marker = fragment.get("layers") == ["N"]

    if len(coords := first(fragment["map"], "").split("/")) == 3:
        zoom, lat, lng = coords
    else:
        zoom, lat, lng = "5/0/0".split("/")

    return {"zoom": zoom, "lng": lng, "lat": lat, "marker": marker}
