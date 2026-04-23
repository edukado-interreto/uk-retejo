from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    ListBlock,
    StreamBlock,
)

from evente.blocks.components import CallToAction, ExtraRichText, FlatFeature
from evente.blocks.widgets import SwiperSlider
from evente.choices.tailwind import (
    Colors,
    Fonts,
    FontSizes,
    FontWeights,
    Lightness,
    TextAlign,
    TextTransform,
)
from evente.mixins import (
    AutoTemplate,
    BgMixin,
    ColorMixin,
    CssMixin,
    FontMixin,
    SettingStructBlock,
    SpacingMixin,
    TextMixin,
    WidthMixin,
)


class SectionBlock(AutoTemplate, BgMixin, SpacingMixin, CssMixin, SettingStructBlock):
    container = BooleanBlock(required=False, default=True, _setting=True)
    effect = ChoiceBlock(
        [("jarallax", _("Parallax"))],
        label=_("Effect"),
        required=False,
        _setting=True,
    )


class SectionHeaderBlock(TextMixin, FontMixin, ColorMixin, SettingStructBlock):
    class Meta:
        _header_default = {
            "font": Fonts.RALEWAY,
            "color": Colors.ZINC,
            "lightness": Lightness.L900,
        }

    def get_default(self):
        """Merge the default values from mixins, base, then concrete block."""
        return self.normalize(
            {
                **super().get_default(),
                **self.meta._header_default,
                **self.meta.default,
            }
        )


class SectionHeaderSubtitle(AutoTemplate, SectionHeaderBlock):
    class Styles(TextChoices):
        FLAT = "flat", _("Flat")
        ROUNDED = "rounded", _("Rounded")
        ELEVATED = "elevated", _("Elevated")

    text = CharBlock(label=_("Text"), required=False)
    style = ChoiceBlock(Styles.choices, default=Styles.FLAT, label=_("Style"))

    class Meta:
        label = _("Subtitle")
        fragment = "#subtitle"
        icon = "h2"
        default = {
            "color": Colors.PRIMARY,
            "lightness": Lightness.L500,
            "text_transform": TextTransform.UPPERCASE,
        }


class SectionHeaderTitle(AutoTemplate, SectionHeaderBlock):
    text = CharBlock(label=_("Text"), required=False)

    class Meta:
        label = _("Title")
        fragment = "#title"
        icon = "h1"
        default = {
            "font": Fonts.UNBOUNDED,
            "font_size": FontSizes.XL4,
            "font_weight": FontWeights.SEMIBOLD,
        }


class SectionHeaderText(AutoTemplate, SectionHeaderBlock):
    text = CharBlock(label=_("Text"), required=False)

    class Meta:
        label = _("Text")
        fragment = "#text"
        icon = "pilcrow"


class SectionHeader(AutoTemplate, TextMixin, SettingStructBlock):
    parts = StreamBlock(
        [
            ("subtitle", SectionHeaderSubtitle()),
            ("title", SectionHeaderTitle()),
            ("text", SectionHeaderText()),
        ]
    )

    class Meta:
        icon = "title"
        default = {
            "parts": [
                ("subtitle", {**SectionHeaderSubtitle().get_default(), "text": ""}),
                ("title", {**SectionHeaderTitle().get_default(), "text": ""}),
                ("text", {**SectionHeaderText().get_default(), "text": ""}),
            ],
            "text_align": TextAlign.CENTER,
        }


class SectionContent(StreamBlock):
    text = ExtraRichText()
    flat_feature = FlatFeature()
    header = SectionHeader()
    call_to_action = CallToAction()

    class Meta:
        collapsed = True


class SectionColumn(WidthMixin, TextMixin, SettingStructBlock):
    content = SectionContent(required=False)

    class Meta:
        group = _("Layout")


class SectionRow(AutoTemplate, SpacingMixin, SettingStructBlock):
    column = ListBlock(SectionColumn())

    class Meta:
        group = _("Layout")
        icon = "dots-horizontal"


class SimpleSection(SectionBlock):
    content = StreamBlock(
        [
            ("header", SectionHeader()),
            ("text", ExtraRichText()),
            ("row", SectionRow()),
        ],
        required=False,
        collapsed=True,
    )

    class Meta:
        group = _("Layout")
        collapsed = True


class BodyContent(StreamBlock):
    section = SimpleSection()
    swiper_slider = SwiperSlider()

    class Meta:
        collapsed = True
