import json
from http import HTTPStatus
from random import choice, randint

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from apps.devel.utils import (
    current_year,
    get_faker,
    mostly,
    random_age_group,
    random_country,
    random_missing_fields,
    random_names,
    to_latin,
)

JSON_NOT_IMPLEMENTED = JsonResponse(
    {"error": "not implemented"}, status=HTTPStatus.NOT_IMPLEMENTED
)


def _participants(k=8, default="pl_PL"):
    for _i in range(k):
        country = random_country()
        fake = get_faker(country, default)
        first_name, last_name = random_names(fake)
        yield {
            "country": country,
            "hidden": mostly(False),
            "first_name": to_latin(first_name),
            "last_name": to_latin(last_name),
        }


@csrf_exempt
def checkcode(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"success": False})
    if code := json.loads(request.body).get("code"):
        if code.endswith("-x"):
            return JsonResponse({"valid": False})
        return JsonResponse(
            {
                "valid": True,
                "member": {
                    "missingFields": random_missing_fields(),
                    "isRegistered": choice([True, False]),
                    "isMember": choice([True, False]),
                    "countryCategory": choice("A B C D".split()),
                    "countryMembershipCategory": randint(1, 4),
                    "ageGroup": random_age_group,
                    "specialCategory": None,
                    "discount": 0,
                },
            }
        )

    return JsonResponse({"valid": False})


def loaddata(request: HttpRequest):
    with open(settings.BASE_DIR / "apps/devel/data/loaddata.json") as payload:
        return JsonResponse(json.loads(payload.read()))


@csrf_exempt
def get_registration(request: HttpRequest):
    with open(settings.BASE_DIR / "apps/devel/data/registration.json") as payload:
        return JsonResponse(json.loads(payload.read()))


@cache_page(60 * 60)
@csrf_exempt
def participants(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"success": False})
    year = json.loads(request.body or b"{}").get("year", 1887)
    if not current_year(year):
        return JsonResponse({"valid": False})
    data = {
        "success": True,
        "participants": list(_participants(k=800)),
    }
    return JsonResponse(data)


@csrf_exempt
def saveform(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def directpayment(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def invitation(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def clearcache(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def query(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def confirmparticipations(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def checkmembersdata(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def updatediscountlist(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def kongresanoj_num(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


# === Admin API views ===


@csrf_exempt
def login(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def getcache(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def deletecachefile(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def getchangestoconfirm(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def previewchangeconfirmationemail(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def sendchangeconfirmationemails(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED


@csrf_exempt
def registermanually(request: HttpRequest):
    return JSON_NOT_IMPLEMENTED
