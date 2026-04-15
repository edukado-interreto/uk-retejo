from functools import wraps
from pathlib import Path

from django.db import OperationalError, close_old_connections, connection
from django.http import HttpRequest
from django_rsgi.serve import serve_file

SQL = "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle'"


def close_idle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("start CLOSE_IDLE ", flush=True)
        close_old_connections()
        with connection.cursor() as cursor:
            cursor.execute(SQL)
            cursor.fetchall()
        print("end CLOSE_IDLE ", flush=True)
        return func(*args, **kwargs)

    return wrapper


# @close_idle
def serve_upload(
    request: HttpRequest,
    path: str | Path,
    document_root: str | Path | None = None,
    **kwargs,
):
    "Add Cache-Control header to django_rsgi.serve_file response."
    response = serve_file(request, path, document_root, **kwargs)
    response.headers["Cache-Control"] = "max-age=7776000, public"
    return response
