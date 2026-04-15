from wagtail import blocks
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from evente.choices import FontAwesomeStyles


def start_with_fa(value):
    if not value.startswith("fa-"):
        ValidationError(
            _("Icon name should start with 'fa-', maybe like fa-%(value)s"),
            params={"value": value},
        )


def no_spaces(value):
    if " " in value:
        ValidationError(_("Icon name shouldn’t contain any space"))


class FontAwesomeField(blocks.ChoiceBlock):
    max_length = 50
    validators = [no_spaces, start_with_fa]
    choices = FontAwesomeStyles.choices
    default = FontAwesomeStyles.REGULAR
