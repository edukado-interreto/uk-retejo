from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    Block,
    BlockGroup,
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    StructBlock,
)
from wagtail.images.blocks import ImageChooserBlock

from evente.choices import tailwind
from evente.utils import snake_case, split_by, uniq


class SettingStructBlock(StructBlock):
    def get_block_settings(self) -> list[str | BlockGroup]:
        mixin_settings = [
            name
            for name, b in self.child_blocks.items()
            if getattr(b.meta, "_setting", False)
        ]
        block_settings = getattr(self.meta, "block_settings", [])
        return uniq(mixin_settings + block_settings)

    def get_form_layout(self) -> BlockGroup:
        children, settings = split_by(
            self.child_blocks.keys(),
            self.get_block_settings(),
        )
        classname = "collapsed" if self.meta.collapsed else ""

        if (form_layout := self.meta.form_layout) is None:
            return BlockGroup(children, settings, classname=classname)
        if isinstance(form_layout, list):
            return BlockGroup(*split_by(form_layout, settings))

        form_layout.children = uniq(children + form_layout.children)
        form_layout.settings = uniq(settings + form_layout.settings)
        return form_layout


class ColorMixin(SettingStructBlock):
    color = ChoiceBlock(
        tailwind.Colors.choices,
        label=_("Color"),
        default=tailwind.Colors.BLACK,
        _setting=True,
    )
    lightness = ChoiceBlock(
        tailwind.Lightness.choices,
        label=_("Lightness"),
        default=tailwind.Lightness.L500,
        _setting=True,
    )


class CssMixin(StructBlock):
    css_classes = CharBlock(
        label=_("CSS classes"),
        default="",
        required=False,
        _setting=True,
    )
    css_style = CharBlock(
        label=_("CSS style"),
        default="",
        required=False,
        _setting=True,
    )


class SpacingMixin(StructBlock):
    margin_top = ChoiceBlock(
        [("mt-[-95px]", "-95px")],
        label=_("Margin top"),
        required=False,
        _setting=True,
    )
    margin_bottom = ChoiceBlock(
        choices=[],
        label=_("Margin bottom"),
        required=False,
        _setting=True,
    )
    padding_top = ChoiceBlock(
        label=_("Padding top"),
        choices=tailwind.PaddingTop.choices,
        default=tailwind.PaddingTop.PT140,
        required=False,
        _setting=True,
    )
    padding_bottom = ChoiceBlock(
        label=_("Padding bottom"),
        choices=tailwind.PaddingBottom.choices,
        default=tailwind.PaddingBottom.PB110,
        required=False,
        _setting=True,
    )


class FlexMixin(StructBlock):
    justify_content = ChoiceBlock(
        tailwind.JustifyContent.choices,
        label=_("Justify content"),
        required=False,
        _setting=True,
    )


class BgColorMixin(StructBlock):
    bg_color = ChoiceBlock(
        tailwind.Colors.choices,
        label=_("Background color"),
        required=False,
        _setting=True,
    )
    bg_lightness = ChoiceBlock(
        tailwind.Lightness.choices,
        label=_("Background color lightness"),
        required=False,
        _setting=True,
    )

    @property
    def background_color(self) -> str:
        if self.bg_color:
            return f"bg-{self.bg_color}-{self.bg_lightness or 900}"
        return ""


class BgMixin(BgColorMixin):
    Position = tailwind.BackgroundPosition
    Repeat = tailwind.BackgroundRepeat
    Size = tailwind.BackgroundSize

    bg_image = ImageChooserBlock(
        label=_("Background image"),
        required=False,
        _setting=True,
    )
    bg_position = ChoiceBlock(
        Position.choices,
        label=_("Background position"),
        required=False,
        _setting=True,
    )
    bg_repeat = ChoiceBlock(
        Repeat.choices,
        label=_("Background repeat"),
        required=False,
        _setting=True,
    )
    bg_size = ChoiceBlock(
        Size.choices,
        label=_("Background size"),
        required=False,
        _setting=True,
    )


class WidthMixin(StructBlock):
    width = ChoiceBlock(
        tailwind.Widths.choices,
        label=_("Width (default)"),
        required=False,
        _setting=True,
    )
    width_sm = ChoiceBlock(
        tailwind.Widths.choices,
        label=_("Width SM"),
        required=False,
        _setting=True,
    )
    width_md = ChoiceBlock(
        tailwind.Widths.choices,
        label=_("Width MD"),
        required=False,
        _setting=True,
    )
    width_lg = ChoiceBlock(
        tailwind.Widths.choices,
        default=tailwind.Widths.W4,
        label=_("Width LG"),
        required=False,
        _setting=True,
    )
    width_xl = ChoiceBlock(
        tailwind.Widths.choices,
        label=_("Width XL"),
        required=False,
        _setting=True,
    )
    width_2xl = ChoiceBlock(
        tailwind.Widths.choices,
        label=_("Width 2XL"),
        required=False,
        _setting=True,
    )


class TextMixin(StructBlock):
    text_align = ChoiceBlock(
        tailwind.TextAlign.choices,
        label=_("Text align"),
        required=False,
        _setting=True,
    )
    text_decoration = ChoiceBlock(
        tailwind.TextDecoration.choices,
        label=_("Text decoration"),
        required=False,
        _setting=True,
    )
    text_transform = ChoiceBlock(
        tailwind.TextTransform.choices,
        label=_("Text transform"),
        required=False,
        _setting=True,
    )


class FontMixin(StructBlock):
    font = ChoiceBlock(
        tailwind.Fonts.choices,
        label=_("Font"),
        required=False,
        _setting=True,
    )
    font_size = ChoiceBlock(
        tailwind.FontSizes.choices,
        label=_("Font size"),
        required=False,
        _setting=True,
    )
    font_weight = ChoiceBlock(
        tailwind.FontWeights.choices,
        label=_("Font weight"),
        required=False,
        _setting=True,
    )


class OnHomepageMixin:
    show_on_homepage = BooleanBlock()


class AutoTemplate(Block):
    def get_template(self, value=None, context=None):
        if template := super().get_template(value, context):
            return template

        template_dir = "/".join(self.__module__.split("."))
        name = snake_case(self.__class__.__name__)

        if partial := getattr(self.meta, "partial", None):
            # Remove the last word of class name
            name = name.rsplit("_", maxsplit=1)[0]
            return "/".join([template_dir, f"{name}.html{partial}"])

        return "/".join([template_dir, f"{name}.html"])
