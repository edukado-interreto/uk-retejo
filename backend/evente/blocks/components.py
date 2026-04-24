from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from evente.choices import FontAwesomeStyles, Flaticons, Colors
from evente.fields import FontAwesomeField
from evente.mixins import AutoTemplate, SettingStructBlock, ColorMixin, SpacingMixin

url_validator = URLValidator()


def fragment_validator(value: str):
    if not value.startswith("#"):
        url_validator(value)


class LinkBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        required=False,
        help_text="Anchor or link to another website page",
        validators=[fragment_validator],
    )
    page = blocks.PageChooserBlock(required=False, help_text="Link to a page")

    class Meta:
        icon = "link"

    def clean(self, value):
        result = super().clean(value)
        if not (result["page"] or result["url"]):
            raise ValidationError(
                "You must specify either an internal page or an external URL"
            )
        return result

    def deconstruct(self):
        return ("evente.blocks.components.LinkBlock", [], self._constructor_kwargs)


class CallToAction(AutoTemplate, SettingStructBlock):
    text = blocks.CharBlock(required=True, help_text="Text to display in the button")
    url = blocks.CharBlock(
        required=False,
        help_text="Anchor or link to another website page",
        validators=[fragment_validator],
    )
    page = blocks.PageChooserBlock(required=False, help_text="Link to a page")
    append_icon = blocks.ChoiceBlock(
        [("arrow-top-right", _("Arrow top right"))],
        default="arrow-top-right",
        label=_("Icon at the end"),
        icon="arrow-right-full",
        required=False,
        _setting=True,
    )

    def clean(self, value):
        result = super().clean(value)
        if not (result["page"] or result["url"]):
            raise ValidationError(
                "You must specify either an internal page or an external URL"
            )
        return result

    class Meta:
        icon = "link-external"


class BaseSocialLink(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Name"), default="")
    href = blocks.CharBlock(
        label=_("Link"),
        default="#",
        validators=[fragment_validator],
    )
    fa_style = FontAwesomeField(
        label=_("Font Awesome style"),
        default=FontAwesomeStyles.BRANDS,
    )
    fa_name = blocks.CharBlock(
        label=_("Font Awesome name"),
        default="fa-globe",
        help_text="https://fontawesome.com/v6/search?ic=free-collection",
    )


class SocialLink(AutoTemplate, BaseSocialLink):
    pass


class ExtraRichText(AutoTemplate, ColorMixin, SpacingMixin, SettingStructBlock):
    content = blocks.RichTextBlock()

    class Meta:
        icon = "pilcrow"


class FlatFeature(AutoTemplate, ColorMixin, SettingStructBlock):
    title = blocks.CharBlock(label=_("Title"))
    text = blocks.CharBlock(label=_("Text"))
    flaticon = blocks.ChoiceBlock(
        Flaticons.choices,
        label=_("Flaticon"),
        required=False,
    )

    class Meta:
        icon = "tick-inverse"
        default = {
            "color": Colors.WHITE,
        }
