from django.utils.translation import gettext_lazy as _
from wagtail.admin.widgets import BaseChooser
from wagtail.blocks import (
    BlockGroup,
    CharBlock,
    ChoiceBlock,
    ChooserBlock,
    ListBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtailmenus.models import FlatMenu

from evente.choices import TailwindColors, TailwindLightness
from evente.mixins import AutoTemplate, SettingStructBlock, WidthMixin, ColorMixin

# Fields


class FlatMenuChooser(BaseChooser):
    choose_one_text = _("Choose a menu")
    choose_another_text = _("Choose another menu")
    link_to_chosen_text = _("Edit this menu")
    icon = "list-ul"
    model = "wagtailmenus.FlatMenu"
    chooser_modal_url_name = "wagtailsnippetchoosers_wagtailmenus_flatmenu:choose"


class FlatMenuChooserBlock(ChooserBlock):
    target_model = "wagtailmenus.FlatMenu"
    widget = FlatMenuChooser()


# Abstract helpers


class ColumnContentStructBlock(ColorMixin, SettingStructBlock):
    margin_top = ChoiceBlock(
        [("mt-0", _("None")), ("mt-3", "3"), ("mt-6", "6")],
        default="mt-0",
        label=_("Top margin"),
        required=False,
        _setting=True,
    )
    margin_bottom = ChoiceBlock(
        [("mb-0", _("None")), ("mb-3", "3"), ("mb-6", "6")],
        default="mb-3",
        label=_("Bottom margin"),
        required=False,
        _setting=True,
    )
    text_size = ChoiceBlock(
        [("", _("Normal")), ("text-xl", _("Big"))],
        default="",
        label=_("Text size"),
        required=False,
        _setting=True,
    )
    text_weight = ChoiceBlock(
        [("", _("Normal")), ("font-semibold", _("Semibold")), ("font-bold", _("Bold"))],
        default="",
        label=_("Text weight"),
        required=False,
        _setting=True,
    )

    class Meta:
        default = {
            "color": TailwindColors.GRAY,
            "lightness": TailwindLightness.L400,
        }


# Blocks


class FooterLogo(SettingStructBlock):
    margin_top = ChoiceBlock(
        [("mt-0", _("None")), ("mt-3", "3"), ("mt-6", "6")],
        default="mt-0",
        label=_("Top margin"),
        required=False,
        _setting=True,
    )
    margin_bottom = ChoiceBlock(
        [("mb-0", _("None")), ("mb-3", "3"), ("mb-6", "6")],
        default="mb-3",
        label=_("Bottom margin"),
        required=False,
        _setting=True,
    )
    logo = ImageChooserBlock()
    href = CharBlock(label=_("Link"), default="", required=False)

    class Meta:
        icon = "pick"


class FooterText(ColumnContentStructBlock):
    text = CharBlock(label=_("Text"))

    class Meta:
        icon = "pilcrow"


class FooterLink(ColumnContentStructBlock):
    text = CharBlock(label=_("Text"))
    href = CharBlock(label=_("Link"))

    class Meta:
        icon = "link"


class FooterMenu(AutoTemplate, ColumnContentStructBlock):
    menu = FlatMenuChooserBlock(target_model=FlatMenu, label=_("Flat menu"))

    class Meta:
        icon = "list-ul"


class FooterMiniGallery(AutoTemplate, ColumnContentStructBlock):
    title = CharBlock(label=_("Title"), default=_("Images"), required=False)
    images = ListBlock(ImageChooserBlock(), label=_("Images"), required=False)

    class Meta:
        icon = "image"


class FooterContent(StreamBlock):
    logo = FooterLogo(label=_("Logo"))
    text = FooterText(label=_("Text"))
    link = FooterLink(label=_("Link"))
    menu = FooterMenu(label=_("Menu"))
    mini_gallery = FooterMiniGallery(label=_("Mini gallery"))


class FooterColumn(AutoTemplate, WidthMixin, SettingStructBlock):
    content = FooterContent(label=_("Content"), required=False, collapsed=True)

    class Meta:
        form_layout = BlockGroup(
            ["content"],
            settings=["width_xl", "width_lg", "width_md"],
        )

    @staticmethod
    def __tw_widths(value):
        widths = ((size, value[f"width_{size}"]) for size in "md lg xl".split())
        return " ".join(f"{size}:{value}" for size, value in widths)

    def get_context(self, value, parent_context=None):
        return {
            **super().get_context(value, parent_context),
            "tw_widths": self.__tw_widths(value),
        }


class FooterLayout(AutoTemplate, StructBlock):
    columns = ListBlock(FooterColumn())

    class Meta:
        icon = "table"


class FooterLayoutSimple(FooterLayout):
    # TODO: replace copyright with bottom and columns
    copyright_text = CharBlock(label=_("Copyright"), default="© ", required=False)


class FooterLayoutTwoColors(FooterLayout):
    pass


class FooterLayoutThreeRows(FooterLayout):
    pass
