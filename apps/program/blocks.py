from wagtail.blocks import RichTextBlock, StreamBlock

from apps.base.blocks import (
    CaptionedImageBlock,
    HeadingBlock,
    ProgramProposalBlock,
    TimelineBlock,
)


class TimelineStreamBlock(StreamBlock):
    timeline = TimelineBlock(blank=True, required=False)
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(icon="pilcrow")
    image_block = CaptionedImageBlock()


class ProgramProposalStreamBlock(StreamBlock):
    program_type = ProgramProposalBlock(blank=True, required=False)
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(icon="pilcrow")
    image_block = CaptionedImageBlock()
