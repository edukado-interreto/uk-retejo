from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from evente.choices import FontAwesomeStyles
from evente.fields import FontAwesomeField
from evente.mixins import AutoTemplate

url_validator = URLValidator()


def fragment_validator(value: str):
    if not value.startswith("#"):
        url_validator(value)


class CallToAction(blocks.StructBlock):
    text = blocks.CharBlock(required=True, help_text="Text to display in the button")
    url = blocks.CharBlock(
        required=False,
        help_text="Anchor or link to another website page",
        validators=[fragment_validator],
    )
    page = blocks.PageChooserBlock(required=False, help_text="Link to a page")

    def clean(self, value):
        result = super().clean(value)
        if not (result["page"] or result["url"]):
            raise ValidationError(
                "You must specify either an internal page or an external URL"
            )
        return result

    @property
    def href(self):
        return self.page.url if self.page else self.url


class SocialLink(AutoTemplate, blocks.StructBlock):
    name = blocks.CharBlock(label=_("Name"), default="")
    href = blocks.CharBlock(
        label=_("Link"),
        default="#",
        validators=[fragment_validator],
    )
    fa_style = FontAwesomeField(
        label=_("Font Awesome style"),
        default=FontAwesomeStyles.BRANDS,
    )
    fa_name = blocks.CharBlock(
        label=_("Font Awesome name"),
        default="fa-globe",
        help_text="https://fontawesome.com/v6/search?ic=free-collection",
    )
