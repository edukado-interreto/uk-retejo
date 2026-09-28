from django.db import models
from wagtail.blocks import ChoiceBlock, StructBlock


class VueModule(models.TextChoices):
    REGISTRATION = "registration", "Aliĝilo"
    EDIT = "edit", "Mendilo"
    PARTICIPANTS = "participants", "Aliĝintoj"
    PRICE = "price", "Kotizoj"


class VueJsBlock(StructBlock):
    vue_module = ChoiceBlock(VueModule.choices, default=VueModule.REGISTRATION)

    class Meta:
        template = "registration/vuejs_block.html"
        icon = "code"

    def get_context(self, value, parent_context=None):
        return {
            **super().get_context(value, parent_context),
            "entrypoint": f"entrypoints/{value['vue_module']}.js",
        }
