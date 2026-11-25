"""Invalidation of the template fragment cache ({% wagtailpagecache %}).

As in EduLand, every fragment key includes CACHE_BURST, so changing that value
invalidates all fragments at once. Here it is a random token stored in the cache
and renewed when editors change content, instead of a fingerprint of the page tree
computed on every request: the header and footer also depend on the menus and the
event settings, which the page tree does not reflect.
"""

from secrets import token_hex

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from wagtail.models import Locale, Page, Site
from wagtail.signals import post_page_move

CACHE_BURST_KEY = "uk:cache_burst"

# Apps whose models (snippets, images, menus, event settings…) the fragments render
CONTENT_APPS = {
    "core",
    "evente",
    "program",
    "wagtaildocs",
    "wagtailimages",
    "wagtailmenus",
}
# Pages are tracked wherever they are defined, with the few other wagtailcore models
# shown on the site. The rest of wagtailcore (revisions, logs, reference index…)
# changes on every draft save without affecting the live site.
CONTENT_MODELS = (Page, Site, Locale)


def cache_burst() -> str:
    return cache.get_or_set(CACHE_BURST_KEY, lambda: token_hex(4), timeout=None)


def bust_cache() -> None:
    cache.delete(CACHE_BURST_KEY)


def _bust_on_content_change(sender, instance, **kwargs):
    if isinstance(instance, CONTENT_MODELS) or sender._meta.app_label in CONTENT_APPS:
        bust_cache()


def _bust_on_page_move(sender, **kwargs):
    # Descendants are moved with a queryset update, without post_save
    bust_cache()


def connect_signals():
    post_save.connect(_bust_on_content_change, dispatch_uid="uk_cache_burst_save")
    post_delete.connect(_bust_on_content_change, dispatch_uid="uk_cache_burst_delete")
    post_page_move.connect(_bust_on_page_move, dispatch_uid="uk_cache_burst_move")
