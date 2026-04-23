from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.blocks import StaticBlock
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField

from evente.blocks.components import SocialLink
from evente.blocks.footers import (
    FooterLayoutSimple,
    FooterLayoutThreeRows,
    FooterLayoutTwoColors,
)
from evente.blocks.headers import HeaderMain, HeaderMobile, HeaderTop
from evente.choices.tailwind import (
    Colors,
    Lightness,
    BackgroundPosition,
    BackgroundRepeat,
    BackgroundSize,
)


def max_one(names):
    return {name: {"max_num": 1} for name in names}


class Dummy(StaticBlock): ...


@register_setting(icon="title")
class EventeHeader(BaseSiteSetting):
    sections = StreamField(
        [
            ("top", HeaderTop(label=_("Top header"))),
            ("main", HeaderMain(label=_("Main header"))),
            ("mobile", HeaderMobile(label=_(""))),
            ("search_panel", Dummy(label=_(""))),
            ("cart_panel", Dummy(label=_(""))),
            ("right_panel", Dummy(label=_(""))),
        ],
        block_counts=max_one(
            ["top", "main", "mobile", "search_panel", "right_panel", "cart_panel"]
        ),
        max_num=6,
        blank=True,
        collapsed=True,
    )
    show_top_on_homepage = models.BooleanField(_("Show top on homepage"), default=False)

    panels = [
        FieldPanel("sections"),
        FieldPanel("show_top_on_homepage"),
    ]


@register_setting(icon="list-ul")
class EventeFooter(BaseSiteSetting):
    bg_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("image"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    bg_color = models.CharField(
        _("Color"),
        choices=Colors,
        blank=True,
    )
    bg_lightness = models.IntegerField(
        _("Lightness"),
        choices=Lightness,
        blank=True,
        null=True,
    )
    bg_position = models.CharField(
        _("Position"),
        choices=BackgroundPosition,
        default=BackgroundPosition.CENTER,
        blank=True,
    )
    bg_repeat = models.CharField(
        _("Repeat"),
        choices=BackgroundRepeat,
        default=BackgroundRepeat.NO_REPEAT,
        blank=True,
    )
    bg_size = models.CharField(
        _("Size"),
        choices=BackgroundSize,
        default=BackgroundSize.COVER,
        blank=True,
    )

    margin_top = models.CharField(
        _("Margin top"),
        choices=[("mt-[-95px]", "-95px")],
        default="",
        blank=True,
    )
    padding_top = models.CharField(
        _("Padding top"),
        choices=[
            ("pt-[80px]", "80px"),
            ("pt-[110px] max-2xl:!pt-[70px]", "110px"),
            ("pt-[130px] max-2xl:!pt-[90px]", "130px"),
            ("pt-[155px] max-2xl:!pt-[100px]", "155px"),
            ("pt-[200px]", "200px"),
        ],
        default="pt-[130px] max-2xl:!pt-[90px]",
        blank=True,
    )

    content = StreamField(
        [
            ("simple", FooterLayoutSimple()),
            ("two_colors", FooterLayoutTwoColors()),
            ("three_rows", FooterLayoutThreeRows()),
        ],
        max_num=1,
        blank=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(["bg_image", "bg_color", "bg_lightness"]),
                FieldRowPanel(["bg_position", "bg_size", "bg_repeat"]),
            ],
            heading=_("Background"),
            classname="collapsed",
        ),
        MultiFieldPanel(
            ["margin_top", "padding_top"],
            heading=_("Spacing"),
            classname="collapsed",
        ),
        FieldPanel("content"),
    ]

    @property
    def background_color(self) -> str:
        if self.bg_color:
            return f"bg-{self.bg_color}-{self.bg_lightness or 900}"
        return ""


@register_setting(icon="code")
class EventeSettings(BaseSiteSetting):
    class Meta:
        verbose_name = _("Evente settings")

    primary_color = models.CharField(
        _("primary color"),
        choices=Colors,
        default=Colors.INDIGO,
    )
    primary_lightness = models.IntegerField(
        _("primary lightness"),
        choices=Lightness,
        default=Lightness.L500,
    )

    @property
    def primary(self):
        return f"--color-{self.primary_color}-{self.primary_lightness}"

    secondary_color = models.CharField(
        _("secondary color"),
        choices=Colors,
        default=Colors.PINK,
    )
    secondary_lightness = models.IntegerField(
        _("secondary lightness"),
        choices=Lightness,
        default=Lightness.L400,
    )

    @property
    def secondary(self):
        return f"--color-{self.secondary_color}-{self.secondary_lightness}"

    logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("logo"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    logo_monochrome = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("logo monochrome"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    social_media = StreamField([("link", SocialLink())], blank=True, collapsed=True)

    panels = [
        FieldRowPanel([FieldPanel("logo"), FieldPanel("logo_monochrome")]),
        FieldRowPanel(
            [
                FieldPanel("primary_color"),
                FieldPanel("primary_lightness"),
                FieldPanel("secondary_color"),
                FieldPanel("secondary_lightness"),
            ]
        ),
        FieldPanel("social_media"),
    ]
