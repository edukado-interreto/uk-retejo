from django import template
from evente.models import EventeSettings
from evente.choices import TailwindColors, TailwindWidth

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
def tw_color(block, obj="text", /, prefix="", opacity=None):
    try:
        color = TailwindColors(block.get(f"{prefix}color"))
    except ValueError:
        return ""
    return color.display(obj, block.get(f"{prefix}lightness"), opacity)


@register.simple_tag()
def tw_widths(block):
    widths = ((size, block.get(f"width_{size}")) for size in TailwindWidth.breakpoints)
    widths = {k: TailwindWidth(v) for k, v in widths if v}
    if default_width := block.get("width"):
        widths = {"": TailwindWidth(default_width), **widths}

    return TailwindWidth.display(widths)


@register.simple_tag()
def tw_spacing(block):
    spacing = ["margin_top", "margin_bottom", "padding_top", "padding_bottom"]
    classes = " ".join(block.get(n) for n in spacing)
    return classes
