from django import template

from evente.choices.tailwind import BREAKPOINTS, Colors, FontSizes, Widths
from evente.mixins import SpacingMixin, FontMixin, TextMixin, BgMixin
from evente.models import EventeSettings

register = template.Library()


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
