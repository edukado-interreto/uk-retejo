from django.utils.translation import gettext, gettext_lazy as _
from wagtail.fields import StreamField
from wagtail.models import Page

from apps.base.blocks import BaseStreamBlock
from apps.base.models import BasePageMixin
from apps.home.blocks import HomeStreamBlock
from config.utils import field_panels


class BasicPage(BasePageMixin, Page):
    body = StreamField(
        BaseStreamBlock(),
        blank=True,
        help_text=_("body"),
    )

    content_panels = field_panels("header_image", "body")


class HomePage(Page):
    body = StreamField(
        HomeStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Use this section to list UK pros.",
    )

    content_panels = field_panels("body")

    def __str__(self):
        return gettext("Homepage")
