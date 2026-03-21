from wagtail.blocks import StreamBlock
from apps.base.blocks import HeroBlock, PresentationBlock, PerksBlock, AboutBlock


class HomeStreamBlock(StreamBlock):
    hero_block = HeroBlock()
    presentation_block = PresentationBlock()
    perks_block = PerksBlock()
    about_block = AboutBlock()
