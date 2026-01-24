from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from apps.base.blocks import BaseStreamBlock
from apps.program.blocks import TimelineStreamBlock


class TimelinePage(Page):
    body = StreamField(TimelineStreamBlock(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [FieldPanel("body")]
