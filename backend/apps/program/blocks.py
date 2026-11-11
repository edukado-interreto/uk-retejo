from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    BlockGroup,
    CharBlock,
    ChoiceBlock,
    DecimalBlock,
    IntegerBlock,
    StructBlock,
)
from wagtail.contrib.typed_table_block.blocks import TypedTable, TypedTableBlock

from evente.blocks import groups
from evente.choices import tailwind


class ExcursionTable(TypedTable):
    """Subclass TypedTable to override its template."""

    template = "program/excursion_table.html"


class ExcursionTableBlock(TypedTableBlock):
    class ExcursionType(TextChoices):
        TUTTAGA = ("T", ("Tuttaga"))
        MATENA = ("M", ("Matena"))
        POSTTAGMEZA = ("P", ("Posttagmeza"))
        VESPERA = ("V", ("Vespera"))

    CAPTION = (
        "T = tuttaga ekskurso; "
        "M = duontaga ekskurso matene; "
        "P = duontaga ekskurso posttagmeze; "
        "V = vespera ekskurso."
    )

    text = CharBlock(label=_("Name"))
    excursion_type = ChoiceBlock(
        choices=ExcursionType.choices,
        label=_("Day"),
        required=False,
    )
    price = DecimalBlock(label=_("Price"), min_value=0, decimal_places=2)

    class Meta:
        label = _("Excursion table")
        icon = "table"

    def value_from_datadict(self, data, files, prefix):
        """Override method to return ExcursionTable instead of TypedTable."""
        table = super().value_from_datadict(data, files, prefix)
        return ExcursionTable(
            columns=table.columns,
            row_data=table.row_data,
            caption=table.caption or self.CAPTION,
        )

    def to_python(self, value):
        """Override method to return ExcursionTable instead of TypedTable."""
        table = super().to_python(value)
        return ExcursionTable(
            columns=table.columns,
            row_data=table.row_data,
            caption=table.caption or self.CAPTION,
        )


class Excursions(StructBlock):
    table = ExcursionTableBlock()

    rest_day = IntegerBlock(label=_("Rest day"), default=5)
    rest_day_color = ChoiceBlock(
        tailwind.Colors.choices,
        label=_("Rest day color"),
        default=tailwind.Colors.GREEN,
    )
    rest_day_lightness = ChoiceBlock(
        tailwind.Lightness.choices,
        label=_("Rest day lightness"),
        default=tailwind.Lightness.L100,
    )

    half_day_color = ChoiceBlock(
        tailwind.Colors.choices,
        label=_("Half day color"),
        default=tailwind.Colors.SLATE,
    )
    half_day_lightness = ChoiceBlock(
        tailwind.Lightness.choices,
        label=_("Half day Lightness"),
        default=tailwind.Lightness.L100,
    )

    class Meta:
        label = _("Excursions")
        group = groups.PROGRAM
        icon = "globe"
        template = "program/excursions.html"
        form_layout = BlockGroup(
            children=["table"],
            settings=[
                "rest_day",
                "rest_day_color",
                "rest_day_lightness",
                "half_day_color",
                "half_day_lightness",
            ],
        )
