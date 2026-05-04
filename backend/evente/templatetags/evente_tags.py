from secrets import token_urlsafe

from django import template
from wagtail.models.pages import Page

from evente.choices.tailwind import BREAKPOINTS, Colors, FontSizes, Widths
from evente.mixins import FlexMixin, SpacingMixin, TextMixin
from evente.models import EventeSettings

register = template.Library()


@register.simple_tag()
def tinyid(size=3):
    """String length is about math.ceil(size * 4/3)."""
    return token_urlsafe(size)


@register.simple_tag()
def getpartial(template, suffix="", modulo=None):
    match (suffix, modulo):
        case (str(), int()):
            raise ValueError(f"Can’t use modulo on a string: {suffix!r}")

        case (int(), int()):
            return f"{template}{(suffix % modulo) or modulo}"

        case _:
            return f"{template}{suffix}"


@register.simple_tag(takes_context=True)
def href(context, block):
    """
    Mirror wagtailcore_tags.pageurl but with plain URL as fallback.
    """
    page = block.get("page")
    url = block.get("url", block.get("href", block.get("link")))

    if page is None and url:
        return url

    if not isinstance(page, Page):
        raise ValueError("pageurl tag expected a Page object, got %r" % page)

    return page.get_url(request=context.get("request"))


@register.inclusion_tag("evente/tags/evente_theme.html", takes_context=True)
def evente_theme(context):
    return {"evente": EventeSettings.for_request(context.get("request"))}


@register.inclusion_tag("evente/tags/evente_css_tags.html")
def evente_css_tags(exclude=""):
    return {"exclude": exclude.split()}


@register.inclusion_tag("evente/tags/evente_js_tags.html")
def evente_js_tags(exclude=""):
    return {"exclude": exclude.split()}


@register.simple_tag()
def tw_color_var(values, /, prefix="", opacity=None):
    if color := values.get(f"{prefix}color"):
        color = Colors(color)
    else:
        return ""
    return color.as_var(values.get(f"{prefix}lightness"))


@register.simple_tag()
def tw_color(values, obj="text", /, prefix="", opacity=None):
    if color := values.get(f"{prefix}color"):
        color = Colors(color)
    else:
        return ""
    return color.display(obj, values.get(f"{prefix}lightness"), opacity)


@register.simple_tag()
def tw_font(block, breakpoints=None):
    family = block.get("font")
    weight = block.get("font_weight")
    size = block.get("font_size")
    sizes = FontSizes(size).dynamic(breakpoints) if size else []
    return " ".join([family, weight, *sizes]).strip()


@register.simple_tag()
def tw_text(block):
    values = (block.get(field) for field in TextMixin.base_blocks)
    return " ".join(val for val in values if val).strip()


@register.simple_tag()
def tw_widths(block):
    widths = ((size, block.get(f"width_{size}")) for size in BREAKPOINTS)
    widths = {k: Widths(v) for k, v in widths if v}
    if default_width := block.get("width"):
        widths = {"": Widths(default_width), **widths}

    return Widths.display(widths)


@register.simple_tag()
def tw_spacing(block) -> str:
    values = (block.get(field) for field in SpacingMixin.base_blocks)
    return " ".join(val for val in values if val).strip()


@register.simple_tag()
def tw_flex(block) -> str:
    values = (block.get(field) for field in FlexMixin.base_blocks)
    return " ".join(val for val in values if val).strip()
