import socket
from functools import partial
from dj_database_url import parse as db_url_parse

parse_db_url = partial(db_url_parse, conn_max_age=600, conn_health_checks=True)


def django_vite_dev_mode(debug: bool) -> bool:
    """Checks if `vite` is running the Docker service.

    Always return False in production
    """
    SERVICE_NAME = "vue"

    if not debug:
        return False

    try:
        return bool(socket.gethostbyname(SERVICE_NAME))
    except socket.gaierror:
        return False
