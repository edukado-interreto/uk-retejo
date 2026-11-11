from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    CharBlock,
    DateBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)

from evente.blocks import groups


class TimelineEventBlock(StructBlock):
    date = DateBlock()
    title = CharBlock(
        blank=True,
        help_text=_("Leave empty to show the day"),
        required=False,
    )
    description = RichTextBlock(blank=True)

    class Meta:
        label = _("Event")
        icon = "date"
        template = "core/blocks/program/timeline_event_block.html"


class TimelineBlock(StreamBlock):
    events = TimelineEventBlock(blank=True, required=False)

    class Meta:
        label = _("Timeline")
        group = groups.PROGRAM
        icon = "calendar-check"
        template = "core/blocks/program/timeline_block.html"


class ProgramProposalTitleBlock(StructBlock):
    title = CharBlock(label=_("Title (day)"))

    class Meta:
        label = _("Day title")
        icon = "h3"


class ProgramProposalItemBlock(StructBlock):
    title = CharBlock()
    deadline = DateBlock(blank=True, required=False)
    description = RichTextBlock(blank=True)

    class Meta:
        label = _("Program type")
        icon = "doc-full"
        template = "core/blocks/program/program_proposal_item_block.html"


class ProgramProposalBlock(StreamBlock):
    title_day = ProgramProposalTitleBlock(blank=True, required=False)
    program_type = ProgramProposalItemBlock(blank=True, required=False)

    class Meta:
        label = _("Program proposals")
        group = groups.PROGRAM
        icon = "tasks"
        template = "core/blocks/program/program_proposal_block.html"
