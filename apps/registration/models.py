from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField
from wagtail.models import Page


class RegistrationPage(RoutablePageMixin, Page):
    class VueModule(models.TextChoices):
        REGISTRATION = "registration", "Aliĝilo"
        EDIT = "edit", "Mendilo"

    body = RichTextField(blank=True)
    vue_module = models.CharField(
        max_length=12, choices=VueModule, default=VueModule.REGISTRATION
    )

    content_panels = Page.content_panels + [FieldPanel("vue_module")]

    @property
    def entrypoint(self):
        return f"src/{self.vue_module}.js"

    @path("<str:unique_id>/")
    def edit_page(self, request, unique_id=None):
        return self.render(request, context_overrides={"unique_id": unique_id})
