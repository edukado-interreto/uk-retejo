from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from apps.home.blocks import HomeStreamBlock


class HomePage(Page):
    body = StreamField(
        HomeStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Use this section to list UK pros.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    content_panels = Page.content_panels + ["body"]
