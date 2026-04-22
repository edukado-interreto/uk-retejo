from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    ListBlock,
    StreamBlock,
)

from evente.blocks.components import FlatFeature, ExtraRichText
from evente.choices import (
    Fonts,
    TailwindColors,
    TailwindLightness,
)
from evente.mixins import (
    AutoTemplate,
    BackgroundMixin,
    ColorMixin,
    CssMixin,
    SettingStructBlock,
    SpacingMixin,
    WidthMixin,
)


class SectionBlock(
    AutoTemplate, BackgroundMixin, SpacingMixin, CssMixin, SettingStructBlock
):
    container = BooleanBlock(required=False, default=True, _setting=True)


class SectionHeaderBlock(ColorMixin, SettingStructBlock):
    font = ChoiceBlock(
        Fonts.choices, default=Fonts.POPPINS, label=_("Font"), _setting=True
    )
    uppercase = BooleanBlock(label=_("Uppercase"), required=False, _setting=True)

    class Meta:
        default = {
            "font": Fonts.POPPINS,
            "color": TailwindColors.ZINC,
            "lightness": TailwindLightness.L900,
            "uppercase": False,
        }

    def get_default(self):
        """Merge the default values from Mixin then concrete block."""
        return self.normalize({**super().get_default(), **self.meta.default})


class SectionHeaderSubtitle(AutoTemplate, SectionHeaderBlock):
    text = CharBlock(label=_("Text"), required=False)
    style = ChoiceBlock(
        [("flat", _("Flat")), ("elevated", _("Elevated"))],
        label=_("Style"),
        default="flat",
    )

    class Meta:
        fragment = "#subtitle"
        default = {
            "color": TailwindColors.PRIMARY,
            "lightness": TailwindLightness.L500,
            "uppercase": True,
        }


class SectionHeaderTitle(AutoTemplate, SectionHeaderBlock):
    text = CharBlock(label=_("Text"), required=False)

    class Meta:
        fragment = "#title"
        default = {"font": Fonts.UNBOUNDED}


class SectionHeaderText(AutoTemplate, SectionHeaderBlock):
    text = CharBlock(label=_("Text"), required=False)

    class Meta:
        fragment = "#text"


class SectionHeader(AutoTemplate, StreamBlock):
    subtitle = SectionHeaderSubtitle(label=_("Subtitle"), icon="h2", required=False)
    title = SectionHeaderTitle(label=_("Title"), icon="h1", required=False)
    text = SectionHeaderText(label=_("Text"), icon="pilcrow", required=False)

    class Meta:
        icon = "title"
        default = [
            ("subtitle", {**SectionHeaderSubtitle().get_default(), "text": ""}),
            ("title", {**SectionHeaderTitle().get_default(), "text": ""}),
            ("text", {**SectionHeaderText().get_default(), "text": ""}),
        ]


class SectionContent(StreamBlock):
    text = ExtraRichText()
    flat_feature = FlatFeature()

    class Meta:
        collapsed = True


class SectionColumn(WidthMixin, SettingStructBlock):
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
            ("title", SectionHeader()),
            ("text", ExtraRichText()),
            ("row", SectionRow()),
        ],
        required=False,
        collapsed=True,
    )
