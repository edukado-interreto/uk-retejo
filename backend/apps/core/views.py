from django.core.files.storage import storages
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.static import serve
from wagtail.embeds.embeds import get_embed
from wagtail.embeds.exceptions import EmbedException


@cache_page(60 * 60 * 24 * 30)
def favicon(_request: HttpRequest):
    return redirect(storages["staticfiles"].url("favicon.ico"), permanent=True)


class BadRequestResponse(HttpResponseBadRequest, JsonResponse):
    def __init__(self, data: str, **kwargs):
        super().__init__({"error": data}, **kwargs)


def api_get_embed(request):
    if (url := request.GET.get("url")) is None:
        return BadRequestResponse("No field 'url' found in body")

    try:
        return HttpResponse(get_embed(url=url).html)
    except EmbedException:
        return BadRequestResponse("No field 'url' found in body")


def serve_upload(
    request: HttpRequest, path: str, document_root=None, show_indexes=False
):
    "Add Cache-Control header to django.views.static.serve response."
    response = serve(request, path, document_root, show_indexes)
    response.headers["Cache-Control"] = "max-age=7776000, public"
    return response
