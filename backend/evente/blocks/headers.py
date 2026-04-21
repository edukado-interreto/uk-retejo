from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.models import Site

from evente.blocks.components import CallToAction
from evente.choices import Flaticons
from evente.mixins import AutoTemplate, OnHomepageMixin


def default_home_page():
    return Site.objects.last().root_page


#### Top Header ####


class HeaderContact(AutoTemplate, blocks.StructBlock):
    text = blocks.CharBlock(label=_("Text"))
    link = blocks.CharBlock(label=_("Link"))
    flaticon = blocks.ChoiceBlock(
        Flaticons.choices,
        label=_("Flaticon"),
        max_length=30,
        required=False,
    )


class HeaderSocialMedia(AutoTemplate, blocks.StaticBlock):
    admin_text = _("Set social media links in Evente settings")


class HeaderTopItems(blocks.StreamBlock):
    contact = HeaderContact()
    social_media = HeaderSocialMedia()

    class Meta:
        block_counts = {"social_media": {"max_num": 1}}


class HeaderTop(AutoTemplate, blocks.StructBlock):
    name = blocks.CharBlock(label=_("Name"), default="Top")
    left = HeaderTopItems(label=_("Left items"), required=False)
    right = HeaderTopItems(label=_("Right items"), required=False)


#### Main Header ####


class HeaderLogo(AutoTemplate, blocks.StructBlock):
    page = blocks.PageChooserBlock(label=_("Home page"), default=default_home_page)
    width = blocks.CharBlock(
        label=_("Width"),
        default="150px",
        help_text=_("CSS value, like '150px' or 'auto'"),
    )
    height = blocks.CharBlock(
        label=_("Height"),
        default="auto",
        help_text=_("CSS value, like '150px' or 'auto'"),
    )


class HeaderMainMenu(AutoTemplate, blocks.StaticBlock):
    pass


class HeaderSearch(AutoTemplate, blocks.StaticBlock):
    pass


class HeaderCart(AutoTemplate, blocks.StaticBlock):
    pass


class HeaderCallToAction(OnHomepageMixin, CallToAction):
    pass


class HeaderMobileButton(AutoTemplate, blocks.StaticBlock):
    pass


class HeaderMainItems(blocks.StreamBlock):
    logo = HeaderLogo()
    main_menu = HeaderMainMenu()
    search = HeaderSearch()
    cart = HeaderCart()
    call_to_action = HeaderCallToAction()
    mobile_button = HeaderMobileButton()


class HeaderMain(AutoTemplate, blocks.StructBlock):
    name = blocks.CharBlock(label=_("Name"), default="Main")
    left = HeaderMainItems(label=_("Left items"), required=False)
    center = HeaderMainItems(label=_("Center items"), required=False)
    right = HeaderMainItems(label=_("Right items"), required=False)
    end = HeaderMainItems(label=_("End items"), required=False)


#### Mobile Menu ####


class HeaderMobileLogo(AutoTemplate, blocks.StructBlock):
    page = blocks.PageChooserBlock(label=_("Home page"), default=default_home_page)
    width = blocks.CharBlock(
        label=_("Width"),
        default="150px",
        help_text=_("CSS value, like '150px' or 'auto'"),
    )
    height = blocks.CharBlock(
        label=_("Height"),
        default="auto",
        help_text=_("CSS value, like '150px' or 'auto'"),
    )


class HeaderMobileSearch(AutoTemplate, blocks.StructBlock):
    page = blocks.PageChooserBlock(label=_("Search page"))
    text = blocks.CharBlock(label=_("Name"), default=_("Search here…"))


class HeaderMobileMainMenu(AutoTemplate, blocks.StaticBlock):
    admin_text = _("")


class HeaderMobileCallToAction(CallToAction):
    pass


class HeaderMobileSocialMedia(AutoTemplate, blocks.StaticBlock):
    admin_text = _("Set social media links in Evente settings")


class HeaderMobileItems(blocks.StreamBlock):
    logo = HeaderMobileLogo()
    search = HeaderMobileSearch()
    main_menu = HeaderMobileMainMenu()
    call_to_action = HeaderMobileCallToAction()
    social_media = HeaderMobileSocialMedia()


class HeaderMobile(AutoTemplate, blocks.StructBlock):
    name = blocks.CharBlock(label=_("Name"), default="Mobile")
    items = HeaderMobileItems(label=_("Items"), required=False)


#### Off-canvas Panels ####


class HeaderPreloader(AutoTemplate, blocks.StaticBlock):
    pass


class HeaderCartPanel(AutoTemplate, blocks.StaticBlock):
    pass


class HeaderPanelRight(AutoTemplate, blocks.StaticBlock):
    pass


class HeaderSearchPanel(AutoTemplate, blocks.StaticBlock):
    pass


class Panels(AutoTemplate):
    preloader = HeaderPreloader()  # full page loading overlay
    cart_panel = HeaderCartPanel()
    panel_right = HeaderPanelRight()  # off canvas menu
    search_panel = HeaderSearchPanel()
