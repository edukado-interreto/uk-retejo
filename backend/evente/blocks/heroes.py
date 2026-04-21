from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from evente.blocks.components import CallToAction
from evente.blocks.widgets import Countdown
from evente.mixins import AutoTemplate, BackgroundMixin, ColorMixin, SettingStructBlock


class HeroItemsSubtitle(AutoTemplate, ColorMixin, SettingStructBlock):
    text = blocks.CharBlock(label=_("Text"), required=False)

    class Meta:
        fragment = "#subtitle"
        default = {"color": ColorMixin.Colors.WHITE}


class HeroItemsTitle(AutoTemplate, ColorMixin, SettingStructBlock):
    text = blocks.CharBlock(label=_("Text"), required=False)

    class Meta:
        fragment = "#title"
        default = {"color": ColorMixin.Colors.WHITE}


class HeroItemsLocation(AutoTemplate, ColorMixin, SettingStructBlock):
    text = blocks.CharBlock(label=_("Text"), required=False)

    class Meta:
        fragment = "#location"
        default = {"color": ColorMixin.Colors.WHITE}


class HeroItemsSocials(AutoTemplate, ColorMixin, SettingStructBlock):
    text = blocks.CharBlock(label=_("Text"), required=False)

    class Meta:
        fragment = "#social_links"
        default = {"color": ColorMixin.Colors.WHITE}


class HeroItemsImage(AutoTemplate, SettingStructBlock):
    image = ImageBlock(label=_("Image"), required=False)

    class Meta:
        fragment = "#image"
        default = {"color": ColorMixin.Colors.WHITE}


class HeroItems(blocks.StreamBlock):
    countdown = Countdown()
    call_to_action = CallToAction()
    subtitle = HeroItemsSubtitle()
    title = HeroItemsTitle()
    location = HeroItemsLocation()
    social_links = HeroItemsSocials()
    image = HeroItemsImage()


class Hero1(AutoTemplate, BackgroundMixin, SettingStructBlock):
    left = HeroItems(required=False)
    right = HeroItems(required=False)


class HeroBlock(blocks.StreamBlock):
    hero_1 = Hero1()

    class Meta:
        icon = "title"
        max_num = 1
