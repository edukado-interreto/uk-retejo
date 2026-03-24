from wagtail.fields import StreamField
from wagtail.models import Page

from apps.base.models import BasePageMixin
from apps.program.blocks import ProgramProposalStreamBlock, TimelineStreamBlock
from config.utils import field_panels


class TimelinePage(BasePageMixin, Page):
    body = StreamField(TimelineStreamBlock(), blank=True, use_json_field=True)

    content_panels = field_panels("header_image", "body")


class ProgramProposalPage(BasePageMixin, Page):
    body = StreamField(ProgramProposalStreamBlock(), blank=True, use_json_field=True)

    content_panels = field_panels("header_image", "body")
