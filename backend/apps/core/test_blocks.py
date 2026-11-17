import unicodedata
from datetime import date

import pytest
from bs4 import BeautifulSoup
from django.utils import translation

from apps.core.blocks import ProgramProposalBlock, TimelineBlock
from apps.core.content_blocks import simple_section_content


@pytest.fixture(autouse=True)
def esperanto():
    with translation.override("eo"):
        yield


def nfc(text: str) -> str:
    """Django's eo catalog has decomposed letters: "dimanc\u0302o", "au\u0306gusto"."""
    return unicodedata.normalize("NFC", text.strip())


def render(block, raw) -> BeautifulSoup:
    return BeautifulSoup(block.render(block.to_python(raw)), "html.parser")


def test_simple_section_content_names():
    names = [name for name, _block in simple_section_content]
    assert names == ["excursion_table", "program_proposal", "timeline", "vue_js"]


def test_timeline_renders_one_item_per_event():
    raw = [
        {
            "type": "events",
            "value": {
                "date": "2027-08-01",
                "title": "Inaŭguro",
                "description": "<p>a</p>",
            },
        },
        {
            "type": "events",
            "value": {"date": "2027-08-02", "title": "", "description": ""},
        },
    ]
    soup = render(TimelineBlock(), raw)

    items = soup.select("ul.timeline > li.day")
    assert len(items) == 2
    # Date formats of config/formats/eo
    assert items[0].select_one("time")["datetime"]
    assert nfc(items[0].select_one(".day-of-week").text) == "Dimanĉo"
    assert items[0].select_one("h3.title").text == "Inaŭguro"
    # Without title, no heading
    assert items[1].select_one("h3.title") is None


def test_timeline_event_date_format():
    raw = [{"type": "events", "value": {"date": "2027-08-02", "description": ""}}]
    soup = render(TimelineBlock(), raw)
    assert nfc(soup.select_one("time").text) == "2-a de aŭgusto"


def test_program_proposal_groups_items_under_day_titles():
    raw = [
        {"type": "title_day", "value": {"title": "Lundo"}},
        {
            "type": "program_type",
            "value": {
                "title": "Prelego",
                "deadline": date(2027, 3, 1).isoformat(),
                "description": "<p>Priskribo</p>",
            },
        },
        {
            "type": "program_type",
            "value": {"title": "Koncerto", "deadline": None, "description": ""},
        },
    ]
    soup = render(ProgramProposalBlock(), raw)

    article = soup.select_one("article.program-proposal")
    assert article.select_one("h2.title-day").text == "Lundo"
    details = article.select(".accordion > details")
    assert len(details) == 2
    assert details[0].select_one("summary h3").text == "Prelego"
    assert details[0].select_one(".badge") is not None
    assert details[1].select_one(".badge") is None
