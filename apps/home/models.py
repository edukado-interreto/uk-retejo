from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from apps.home.blocks import HomeStreamBlock
from apps.base.blocks import BaseStreamBlock


class BasicPage(Page):
    body = StreamField(
        BaseStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text=_("body"),
    )

    content_panels = Page.content_panels + [FieldPanel("body")]


class HomePage(Page):
    body = StreamField(
        HomeStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Use this section to list UK pros.",
    )

    content_panels = Page.content_panels + [FieldPanel("body")]
