from django.core.exceptions import ImproperlyConfigured
from django.db import models
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField
from wagtail.models import Page

from config.utils import field_panels
from evente.models import BasePageMixin


class VuePage(BasePageMixin, RoutablePageMixin, Page):
    class VueModule(models.TextChoices):
        REGISTRATION = "registration", "Aliĝilo"
        EDIT = "edit", "Mendilo"
        PARTICIPANTS = "participants", "Aliĝintoj"
        PRICE = "price", "Kotizoj"

    body = RichTextField(blank=True)

    vue_module = models.CharField(
        choices=VueModule.choices, default=VueModule.REGISTRATION
    )

    content_panels = field_panels("header_image", "body", "vue_module")

    @property
    def entrypoint(self):
        if not hasattr(self, "vue_module"):
            raise ImproperlyConfigured("A VuePage must have a vue_module field.")
        return f"entrypoints/{self.vue_module}.js"

    @path("<str:unique_id>/")
    def edit_page(self, request, unique_id=None):
        return self.render(request, context_overrides={"unique_id": unique_id})
