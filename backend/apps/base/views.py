from django.http import HttpRequest
from django.views.static import serve


def serve_upload(
    request: HttpRequest, path: str, document_root=None, show_indexes=False
):
    "Add Cache-Control header to django.views.static.serve response."
    response = serve(request, path, document_root, show_indexes)
    response.headers["Cache-Control"] = "max-age=7776000, public"
    return response
