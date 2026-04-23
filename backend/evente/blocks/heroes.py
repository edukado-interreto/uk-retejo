from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from evente.blocks.components import CallToAction
from evente.blocks.widgets import Countdown
from evente.mixins import (
    AutoTemplate,
    BgMixin,
    ColorMixin,
    SettingStructBlock,
    TextMixin,
    FontMixin,
)
from evente.choices.tailwind import Colors


class BaseHeroItemBlock(TextMixin, FontMixin, ColorMixin, SettingStructBlock):
    text = blocks.CharBlock(label=_("Text"), required=False)

    class Meta:
        _base_default = {
            "color": Colors.WHITE,
        }

    def get_default(self):
        """Merge the default values from mixins, base, then concrete block."""
        return self.normalize(
            {
                **super().get_default(),
                **self.meta._base_default,
                **self.meta.default,
            }
        )


class HeroItemsSubtitle(AutoTemplate, BaseHeroItemBlock):
    class Meta:
        fragment = "#subtitle"


class HeroItemsTitle(AutoTemplate, BaseHeroItemBlock):
    class Meta:
        fragment = "#title"


class HeroItemsLocation(AutoTemplate, BaseHeroItemBlock):
    class Meta:
        fragment = "#location"


class HeroItemsSocials(AutoTemplate, BaseHeroItemBlock):
    class Meta:
        fragment = "#social_links"


class HeroItemsImage(AutoTemplate, SettingStructBlock):
    image = ImageBlock(label=_("Image"), required=False)

    class Meta:
        fragment = "#image"
        default = {"color": Colors.WHITE}


class HeroItems(blocks.StreamBlock):
    countdown = Countdown()
    call_to_action = CallToAction()
    subtitle = HeroItemsSubtitle()
    title = HeroItemsTitle()
    location = HeroItemsLocation()
    social_links = HeroItemsSocials()
    image = HeroItemsImage()


class Hero1(AutoTemplate, BgMixin, SettingStructBlock):
    left = HeroItems(required=False)
    right = HeroItems(required=False)


class HeroBlock(blocks.StreamBlock):
    hero_1 = Hero1()

    class Meta:
        icon = "title"
        max_num = 1
        collapsed = True
