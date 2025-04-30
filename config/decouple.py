import re
from collections import ChainMap
from pathlib import Path

from decouple import AutoConfig, Config, RepositoryEnv, RepositorySecret

__all__ = ["NamedEmail", "config"]


class NamedEmail:
    """Process email in angle brackets with full name before it.

    Example: NamedEmail()(" Name <n@x.eu> ") == ("Name", "n@x.eu")
    """

    RE_NAME = r"(?P<name>\b.+)"
    RE_EMAIL = r"(?P<email>\S+@\S+\.\w+)"
    RE = re.compile(rf"\s*{RE_NAME} <{RE_EMAIL}>\s*")

    def __init__(self, post_process=tuple):
        self.post_process = post_process

    def _match(self, value):
        return self.RE.match(value)

    def __call__(self, value):
        _match = self._match(value)
        if _match is None:
            return self.post_process()
        if self.post_process == dict:
            return self.post_process(_match.groupdict())
        return self.post_process(_match.groups())


if Path("/run/secrets/").exists():
    # Docker Swarm
    config = Config(RepositorySecret())
else:
    # Local development
    config = Config(RepositoryEnv(".env.django"))
