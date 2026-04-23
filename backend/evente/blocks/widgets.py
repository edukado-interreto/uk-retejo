from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from evente.choices import TimeUnits
from evente.mixins import (
    AutoTemplate,
    BgColorMixin,
    ColorMixin,
    SettingStructBlock,
    TextMixin,
)
from evente.choices.tailwind import TextTransform


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
        icon = "logout"
        group = _("Widgets")
        collapsed = True
        default = {"text_transform": TextTransform.UPPERCASE}
