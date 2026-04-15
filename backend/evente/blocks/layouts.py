from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    BlockGroup,
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    StreamBlock,
)

from evente.choices import (
    Fonts,
    TailwindColors,
    TailwindLightness,
)
from evente.mixins import (
    AutoTemplate,
    BackgroundMixin,
    CssMixin,
    SettingStructBlock,
    SpacingMixin,
)


class SectionBlock(
    AutoTemplate, BackgroundMixin, SpacingMixin, CssMixin, SettingStructBlock
):
    pass


class SectionHeaderBlock(SettingStructBlock):
    font = ChoiceBlock(Fonts.choices, default=Fonts.POPPINS, label=_("Font"))
    color = ChoiceBlock(
        [
            *TailwindColors.choices,
        ],
        default=TailwindColors.ZINC,
        label=_("Color"),
    )
    lightness = ChoiceBlock(
        TailwindLightness.choices,
        default=TailwindLightness.L900,
        label=_("Lightness"),
    )
    uppercase = BooleanBlock(label=_("Uppercase"), required=False)

    def get_form_layout(self):
        block_settings: list[str | BlockGroup] = [
            "font",
            "color",
            "lightness",
            "uppercase",
        ]

        return BlockGroup(
            list(self.child_blocks.keys() ^ set(block_settings)),
            settings=block_settings,
        )

    @staticmethod
    def __text_color(value):
        if value["color"].endswith("ary"):
            return f"text-{value['color']}"
        return f"text-{value['color']}-{value['lightness']}"

    def get_context(self, value, parent_context=None):
        return {
            **super().get_context(value, parent_context),
            "text_color": self.__text_color(value),
        }

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
        collapsed = True
        default = [
            ("subtitle", {**SectionHeaderSubtitle().get_default(), "text": ""}),
            ("title", {**SectionHeaderTitle().get_default(), "text": ""}),
            ("text", {**SectionHeaderText().get_default(), "text": ""}),
        ]


class SimpleSection(SectionBlock):
    content = StreamBlock(
        [
            ("title", SectionHeader()),
        ],
        required=False,
    )
