from pathlib import Path

from django.shortcuts import redirect
from django.urls import path

from apps.base.views import serve_upload

EVENTE_DEMO = (Path(__file__).parent / "demo").resolve()

urlpatterns = [
    path("<path:path>", serve_upload, kwargs={"document_root": EVENTE_DEMO}),
    path("", lambda rq: redirect("index.html")),
]
