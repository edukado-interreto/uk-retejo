from django.utils.translation import gettext_lazy as _
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path
from wagtail.fields import StreamField
from wagtail.models import Page

from apps.base.models import BasePageMixin
from config.utils import field_panels
from evente.blocks.heroes import HeroBlock
from evente.blocks.layouts import BodyContent
from evente.models import EventPageMixin


class HomePage(EventPageMixin, Page):
    hero = StreamField(
        HeroBlock,
        verbose_name=_("hero"),
        blank=True,
    )
    body = StreamField(
        BodyContent,
        verbose_name=_("body"),
        blank=True,
    )

    content_panels = field_panels("event", "hero", "body")


class SimplePage(BasePageMixin, RoutablePageMixin, Page):
    body = StreamField(
        BodyContent,
        verbose_name=_("body"),
        blank=True,
    )

    content_panels = field_panels("header_image", "body")

    class Meta:
        verbose_name = "Page"

    @re_path(r"^(?P<unique_id>[0-9a-f]{32,38})/$")
    def mendilo(self, request, unique_id=None):
        """Assuming ID is hexadecimal string of length 32 to 38."""
        ctx = {"unique_id": unique_id} if unique_id else None
        return self.render(request, context_overrides=ctx)
