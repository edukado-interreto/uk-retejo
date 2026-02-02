from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from apps.program.blocks import ProgramProposalStreamBlock, TimelineStreamBlock


class TimelinePage(Page):
    body = StreamField(TimelineStreamBlock(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [FieldPanel("body")]


class ProgramProposalPage(Page):
    body = StreamField(ProgramProposalStreamBlock(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [FieldPanel("body")]
