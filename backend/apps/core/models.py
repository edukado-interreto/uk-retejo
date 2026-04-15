from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from wagtail.models import Page

from apps.base.models import BasePageMixin
from config.utils import field_panels
from evente.blocks.layouts import SimpleSection


class SimplePage(BasePageMixin, Page):
    body = StreamField(
        [("section", SimpleSection())],
        verbose_name=_("body"),
        blank=True,
    )

    content_panels = field_panels("header_image", "body")
