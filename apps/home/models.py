from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path

from apps.home.blocks import HomeStreamBlock


class BasicPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]


class HomePage(Page):
    body = StreamField(
        HomeStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Use this section to list UK pros.",
    )

    content_panels = Page.content_panels + [FieldPanel("body")]


class RegistrationPage(RoutablePageMixin, Page):
    body = RichTextField(blank=True)
    raw_html = models.TextField(blank=True, default="")

    content_panels = Page.content_panels + [FieldPanel("raw_html")]

    @path("<str:unique_id>/")
    def edit_page(self, request, unique_id=None):
        return self.render(request, context_overrides={"unique_id": unique_id})
