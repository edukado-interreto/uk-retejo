import re


def split_by(blocks, setting_blocks):
    settings = set(setting_blocks)
    return ([b for b in blocks if b not in settings], setting_blocks)


def snake_case(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def uniq(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]
