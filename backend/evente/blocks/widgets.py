from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from evente.choices import TimeUnits
from evente.choices.tailwind import TextTransform
from .components import BaseSocialLink, LinkBlock, CallToAction
from evente.mixins import (
    AutoTemplate,
    BgColorMixin,
    ColorMixin,
    SettingStructBlock,
    TextMixin,
)


class CountdownUnit(blocks.StructBlock):
    unit = blocks.ChoiceBlock(TimeUnits.choices, label=_("Unit"))
    text = blocks.TextBlock(label=_("Text"))

    class Meta:
        icon = "decimal"
        collapsed = True


class Countdown(AutoTemplate, TextMixin, ColorMixin, SettingStructBlock):
    start = blocks.DateTimeBlock(label=_("Start"))
    items = blocks.ListBlock(CountdownUnit, label=_("Items"))

    class Meta:
        icon = "history"
        collapsed = True
        default = {
            "color": "white",
            "text_transform": TextTransform.UPPERCASE,
            "items": [
                {"unit": "days", "text": "Days"},
                {"unit": "hours", "text": "Hrs"},
                {"unit": "minutes", "text": "Mins"},
                {"unit": "seconds", "text": "Secs"},
            ],
        }

    @classmethod
    def interval(cls, value):
        has_seconds = TimeUnits.SECONDS in cls.used_units(value)
        ms = 1000 if has_seconds else 60000
        return ms / 2

    @classmethod
    def used_units(cls, value):
        return [i["unit"] for i in value["items"]]

    def get_context(self, value, parent_context=None):
        return {
            **super().get_context(value, parent_context),
            "interval": self.interval(value),
            "used_units": repr(self.used_units(value)),
            "units": [u for u in TimeUnits if u in self.used_units(value)],
        }


class SwiperSlide(AutoTemplate, SettingStructBlock):
    text = blocks.TextBlock()


class SwiperSlider(
    AutoTemplate, TextMixin, BgColorMixin, ColorMixin, SettingStructBlock
):
    slides = blocks.ListBlock(SwiperSlide())

    class Meta:
        label = _("Swiper slider")
        icon = "logout"
        group = _("Widgets")
        collapsed = True
        default = {"text_transform": TextTransform.UPPERCASE}


class PersonCard(AutoTemplate, SettingStructBlock):
    class Styles(TextChoices):
        CARD = "team1", _("Card")
        ALBUM = "team2", _("Album")
        ROUND = "team3", _("Round")
        SHAPE = "team5", _("Shape")

    full_name = blocks.CharBlock(label=_("Name"))
    position = blocks.CharBlock(label=_("Position"), required=False)
    image = ImageBlock(label_=("Image"), required=False)
    link = LinkBlock(label_=("Link"), required=False)
    social_links = blocks.ListBlock(BaseSocialLink(), required=False)

    style = blocks.ChoiceBlock(
        Styles.choices,
        default=Styles.CARD,
        label=_("Style"),
        _setting=True,
    )

    class Meta:
        label = _("Person card")
        group = _("Widgets")
        collapsed = True
        icon = "user"

    def get_template(self, value=None, context=None):
        template = super().get_template(value, context)
        return f"{template}#{value['style']}"


class PricingCard(AutoTemplate, SettingStructBlock):
    subtitle = blocks.CharBlock(label=_("Subtitle"))
    price = blocks.CharBlock(label=_("Price"))
    perks = blocks.ListBlock(
        blocks.CharBlock(label=_("Perk"), icon="check"), required=False
    )
    buttons = blocks.ListBlock(CallToAction(), required=False)

    class Meta:
        label = _("Pricing card")
        group = _("Widgets")
        collapsed = True
        icon = "decimal"
