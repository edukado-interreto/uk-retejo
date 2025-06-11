import json

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def loaddata(request: HttpRequest):
    with open(settings.CONFIG_DIR / "dev" / "data" / "loaddata.json") as payload:
        return JsonResponse(json.loads(payload.read()))


@csrf_exempt
def get_registration(request: HttpRequest):
    with open(settings.CONFIG_DIR / "dev" / "data" / "registration.json") as payload:
        return JsonResponse(json.loads(payload.read()))
