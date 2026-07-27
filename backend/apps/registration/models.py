from django.core.exceptions import ImproperlyConfigured
from django.db import models
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField
from wagtail.models import Page

from apps.base.models import BasePageMixin
from config.utils import field_panels


class VueMixin(Page):
    class Meta:
        abstract = True

    body = RichTextField(blank=True)

    @property
    def entrypoint(self):
        if not hasattr(self, "vue_module"):
            raise ImproperlyConfigured("A VuePage must have a vue_module field.")
        return f"src/{self.vue_module}.js"


class VuePage(VueMixin, BasePageMixin, Page):
    class VueModule(models.TextChoices):
        PARTICIPANTS = "participants", "Aliĝintoj"
        PRICE = "price", "Kotizoj"

    vue_module = models.CharField(choices=VueModule, default=VueModule.PARTICIPANTS)

    content_panels = field_panels("header_image", "body", "vue_module")


class RegistrationPage(VueMixin, BasePageMixin, RoutablePageMixin, Page):
    class VueModule(models.TextChoices):
        REGISTRATION = "registration", "Aliĝilo"
        EDIT = "edit", "Mendilo"

    _vue_module = VueModule.REGISTRATION

    @property
    def vue_module(self) -> VueModule:
        return self._vue_module

    @vue_module.setter
    def vue_module(self, value: VueModule):
        self._vue_module = value
        return self._vue_module

    content_panels = field_panels("header_image", "body")

    @path("mendilo/<str:unique_id>/")
    def edit_page(self, request, unique_id=None):
        self.vue_module = self.VueModule.EDIT
        return self.render(request)
