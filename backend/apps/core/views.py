import json

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from wagtail.embeds.embeds import get_embed
from wagtail.embeds.exceptions import EmbedException


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
