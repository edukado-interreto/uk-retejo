from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import ChoiceBlock, StructBlock


class VueModule(models.TextChoices):
    REGISTRATION = "registration", "Aliĝilo"
    EDIT = "edit", "Mendilo"
    PARTICIPANTS = "participants", "Aliĝintoj"
    PRICE = "price", "Kotizoj"


class VueJsBlock(StructBlock):
    vue_module = ChoiceBlock(VueModule.choices, default=VueModule.REGISTRATION)

    class Meta:
        label = _("VueJS module")
        icon = "code"
        group = _("Expert")
        template = "registration/vuejs_block.html"

    def get_context(self, value, parent_context=None):
        return {
            **super().get_context(value, parent_context),
            "entrypoint": f"entrypoints/{value['vue_module']}.js",
        }
