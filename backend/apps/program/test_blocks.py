from decimal import Decimal

import pytest
from bs4 import BeautifulSoup
from django.http import QueryDict
from django.template import Context, Template
from wagtail.blocks import StreamBlock

from apps.program.blocks import Excursions, ExcursionTable, ExcursionTableBlock

COLUMNS = [
    {"type": "text", "heading": ""},
    {"type": "excursion_type", "heading": "Lundo"},
    {"type": "price", "heading": "Prezo"},
]


def table_data(caption=""):
    return {
        "columns": COLUMNS,
        "rows": [
            {"values": ["Urbovizito", "M", "12.5"]},
            {"values": ["Kastelo", "T", "40"]},
        ],
        "caption": caption,
    }


@pytest.mark.parametrize(
    "caption, expected",
    [("", ExcursionTableBlock.CAPTION), ("Propra", "Propra")],
)
def test_to_python_returns_excursion_table(caption, expected):
    table = ExcursionTableBlock().to_python(table_data(caption))
    assert isinstance(table, ExcursionTable)
    assert table.caption == expected
    assert table.template == "program/excursion_table.html"


def test_value_from_datadict_returns_excursion_table():
    block = ExcursionTableBlock()
    data = QueryDict(mutable=True)
    data.update(
        {
            "table-caption": "",
            "table-column-count": "1",
            "table-row-count": "1",
            "table-column-0-type": "text",
            "table-column-0-order": "0",
            "table-column-0-deleted": "",
            "table-column-0-heading": "Nomo",
            "table-row-0-order": "0",
            "table-row-0-deleted": "",
            "table-cell-0-0": "Urbovizito",
        }
    )
    table = block.value_from_datadict(data, {}, "table")
    assert isinstance(table, ExcursionTable)
    assert table.caption == ExcursionTableBlock.CAPTION
    assert [row[0].value for row in table.rows] == ["Urbovizito"]


def test_excursion_type_choices():
    assert ExcursionTableBlock.ExcursionType.values == ["T", "M", "P", "V"]


def render_in_stream(raw) -> BeautifulSoup:
    """Render as in a page: excursion_table.html reads the loop variable `block`."""
    stream = StreamBlock([("excursion_table", Excursions())])
    value = stream.to_python([{"type": "excursion_table", "value": raw}])
    template = Template(
        "{% load wagtailcore_tags %}"
        "{% for block in value %}{% include_block block %}{% endfor %}"
    )
    return BeautifulSoup(template.render(Context({"value": value})), "html.parser")


def test_excursions_render():
    soup = render_in_stream({"table": table_data(), "rest_day": 1})

    table = soup.select_one("table.excursions")
    assert table.caption.text == ExcursionTableBlock.CAPTION
    headings = table.select("thead th")
    assert len(headings) == 3
    # Empty heading is kept invisible, for the layout
    assert headings[0].select_one("span.opacity-0") is not None
    # Rest day = first day, i.e. second column
    assert "restday" in headings[1]["class"]
    assert "bg-green-100" in headings[1]["class"]

    rows = table.select("tbody tr")
    assert [row.th.text.strip() for row in rows] == ["Urbovizito", "Kastelo"]
    prices = [row.select("td")[-1].text.strip() for row in rows]
    assert prices == ["12,50", "40"]
    # The rest day column is highlighted in every row
    assert all("restday" in row.select("td")[0]["class"] for row in rows)


def test_excursions_half_day_rows():
    data = table_data()
    data["rows"].append({"values": ["Duontaga promeno", "P", "5"]})
    soup = render_in_stream({"table": data, "half_day_color": "blue"})

    rows = soup.select("tbody tr")
    assert not rows[0].get("class")
    assert rows[-1]["class"] == ["halfday", "bg-blue-100"]


def test_excursions_defaults():
    defaults = Excursions().get_default()
    assert defaults["rest_day"] == 5
    assert defaults["rest_day_color"] == "green"
    assert defaults["half_day_color"] == "slate"


def test_price_is_decimal():
    table = ExcursionTableBlock().to_python(table_data())
    first_row = next(iter(table.rows))
    assert first_row[2].value == Decimal("12.5")
