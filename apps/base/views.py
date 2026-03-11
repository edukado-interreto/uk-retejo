from pathlib import Path

from django.http import HttpRequest
from django_rsgi.serve import serve_file


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

