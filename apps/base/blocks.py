from django.core.exceptions import ValidationError
from django.utils.timezone import now
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
from wagtail.images.blocks import ImageBlock


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


class BaseStreamBlock(StreamBlock):
    hero_block = HeroBlock()
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(icon="pilcrow")
    image_block = CaptionedImageBlock()
    embed_block = EmbedBlock(
        help_text="Insert a URL to embed. For example, https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
    )
