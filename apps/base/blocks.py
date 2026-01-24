from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    DateBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock, ImageChooserBlock

from apps.base.models import FontAwesomeIcon


class CallToActionBlock(StructBlock):
    url = URLBlock(required=False, help_text="Link to another website page")
    page = PageChooserBlock(required=False, help_text="Link to a page")
    text = CharBlock(required=True, help_text="Text to display in the button")

    def clean(self, value):
        result = super().clean(value)
        if not (result["page"] or result["url"]):
            raise ValidationError(
                "You must specify either an internal page or an external URL"
            )
        return result


class CountdownBlock(StructBlock):
    title = CharBlock(required=True, help_text="Countdown title")
    subtitle = CharBlock(
        required=False, help_text="Countdown sub-title (actually above)"
    )


class CaptionedImageBlock(StructBlock):
    image = ImageBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "base/blocks/captioned_image_block.html"


class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a heading size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "base/blocks/heading_block.html"


class HeroBlock(StructBlock):
    title = CharBlock(classname="title", required=True)
    dates = CharBlock(blank=True, required=False)
    start_date = DateBlock(blank=True, required=False)
    end_date = DateBlock(blank=True, required=False)
    location = CharBlock(blank=True, required=False)
    background = ImageBlock(blank=True, required=False)
    call_to_action = CallToActionBlock(blank=True, required=False)
    countdown = CountdownBlock(blank=True, required=False)

    class Meta:
        icon = "home"
        template = "base/blocks/hero_block.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["started"] = value["start_date"] >= now().date()
        return context


class PresentationBlock(StructBlock):
    title = CharBlock(classname="title", required=True)
    subtitle = CharBlock(classname="subtitle", required=True)
    main_image = ImageBlock(required=True)
    first_image = ImageBlock(required=False)
    second_image = ImageBlock(required=False)
    third_image = ImageBlock(required=False)
    paragraph = RichTextBlock(icon="pilcrow")
    button_text = CharBlock(required=False, help_text="Text on the More button")
    button_page = PageChooserBlock(required=False, help_text="Link to a page")

    class Meta:
        icon = "info-circle"
        template = "base/blocks/presentation_block.html"


class PerkBlock(StructBlock):
    title = CharBlock(classname="title", required=True)
    paragraph = RichTextBlock(icon="pilcrow")
    icon = ChoiceBlock(choices=FontAwesomeIcon.get_icon_choices)
    color = ChoiceBlock(
        choices=[
            ("", "Select a color"),
            ("warning", "Yellow"),  # text-warning
            ("info", "Blue"),  # text-info
            ("success", "Green"),  # text-success
            ("secondary", "Pink"),  # text-secondary
        ]
    )

    class Meta:
        icon = "check"
        template = "base/blocks/perk_block.html"


class PerksStreamBlock(StreamBlock):
    perk = PerkBlock(blank=True, required=False)


class VideoBlock(EmbedBlock):
    help_text = (
        "Insert an URL to embed. For example, https://www.youtube.com/watch?v=xm4qTLcXKc4",
    )
    icon = "media"
    max_width = 640
    max_height = 360


class PerksBlock(StructBlock):
    title = CharBlock(classname="title", required=True)
    background = ImageBlock(blank=True, required=False)
    videos = StreamBlock([("video", VideoBlock())])
    perks = PerksStreamBlock()

    class Meta:
        icon = "circle-check"
        template = "base/blocks/perks_block.html"


class FactBlock(StructBlock):
    title = CharBlock()
    description = CharBlock()
    icon = ChoiceBlock(choices=FontAwesomeIcon.get_icon_choices)

    class Meta:
        template = "base/blocks/fact_block.html"


class FactsStreamBlock(StreamBlock):
    fact = FactBlock(blank=True, required=False)

    class Meta:
        icon = "tasks"
        template = "base/blocks/facts_block.html"


class PictureWallStreamBlock(StreamBlock):
    image = ImageChooserBlock(required=True)

    class Meta:
        icon = "image"
        template = "base/blocks/picture_wall_block.html"


class AboutBlock(StructBlock):
    title = CharBlock(blank=True, required=False)
    subtitle = CharBlock(blank=True, required=False)
    facts = FactsStreamBlock(blank=True, required=False)
    pictures = PictureWallStreamBlock(blank=True, required=False)
    event_map = URLBlock(blank=True, required=False)
    directions = RichTextBlock(blank=True, required=False)

    class Meta:
        icon = "globe"
        template = "base/blocks/about_block.html"


class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(icon="pilcrow")
    image_block = CaptionedImageBlock()
    embed_block = EmbedBlock(
        help_text="Insert a URL to embed. For example, https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
    )


class TimelineEventBlock(StructBlock):
    date = DateBlock()
    title = CharBlock(
        blank=True,
        help_text=_("Lasi malplene por afiŝi tagon"),
        required=False,
    )
    description = RichTextBlock(blank=True)

    class Meta:
        template = "base/blocks/timeline_event_block.html"


class TimelineBlock(StreamBlock):
    events = TimelineEventBlock(blank=True, required=False)

    class Meta:
        icon = "calendar-check"
        template = "base/blocks/timeline_block.html"
