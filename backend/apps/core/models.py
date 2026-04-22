from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import Page

from apps.base.models import BasePageMixin
from config.utils import field_panels
from evente.blocks.heroes import HeroBlock
from evente.blocks.layouts import SimpleSection


class CustomImage(AbstractImage):
    # Add any extra fields to image here
    pass


class HomePage(Page):
    hero = StreamField(
        HeroBlock,
        verbose_name=_("hero"),
        blank=True,
    )
    body = StreamField(
        [("section", SimpleSection())],
        verbose_name=_("body"),
        blank=True,
    )

    content_panels = field_panels("hero", "body")


class SimplePage(BasePageMixin, Page):
    body = StreamField(
        [("section", SimpleSection())],
        verbose_name=_("body"),
        blank=True,
    )

    content_panels = field_panels("header_image", "body")
