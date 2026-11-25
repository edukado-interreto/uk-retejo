from django.conf import settings
from wagtail.models import Site
from wagtailmenus.models import FlatMenu

from apps.core.cache import cache_burst

EXPORTED_SETTINGS = ["ENVIRONMENT", "GOATCOUNTER_URL", "TEMPLATE_CACHE_TTL"]


def app(request):
    return {
        "flat_menus": get_menu_handles(request),
        "CACHE_BURST": cache_burst(),
        **{s: getattr(settings, s, None) for s in EXPORTED_SETTINGS},
    }


def get_menu_handles(request, order="handle") -> list[str]:
    site = Site.find_for_request(request)
    flat_menu_handles = (
        FlatMenu.objects.filter(site=site)
        .order_by(order)
        .values_list("handle", flat=True)
    )
    return [str(handle) for handle in flat_menu_handles]
