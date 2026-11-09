from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_pattern_library_menu_item():
    return MenuItem(
        _("Pattern library"),
        reverse("pattern_library:index"),
        icon_name="view",
        order=550,  # After Snippets (500)
    )
