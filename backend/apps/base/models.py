from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.snippets.models import register_snippet


@register_snippet
class FontAwesomeIcon(models.Model):
    name = models.CharField(_("name"), max_length=20, help_text="Uzantoj, Tero,…")
    css_class = models.CharField(
        _("CSS class"),
        max_length=50,
        help_text="'fa-regular fa-users'",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "FontAwesome ikono"
        verbose_name_plural = "FontAwesome ikonoj"

    def __str__(self):
        return self.name

    @classmethod
    def get_icon_choices(cls):
        return cls.objects.values_list("css_class", "name")
