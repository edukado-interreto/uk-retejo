from wagtail.fields import StreamField
from wagtail.models import Page

from apps.program.blocks import ProgramProposalStreamBlock, TimelineStreamBlock
from config.utils import field_panels


class TimelinePage(Page):
    body = StreamField(TimelineStreamBlock(), blank=True, use_json_field=True)

    content_panels = field_panels("body")


class ProgramProposalPage(Page):
    body = StreamField(ProgramProposalStreamBlock(), blank=True, use_json_field=True)

    content_panels = field_panels("body")
