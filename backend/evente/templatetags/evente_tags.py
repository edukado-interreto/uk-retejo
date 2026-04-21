from django import template
from evente.models import EventeSettings
from evente.choices import TailwindColors

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
def tw_color(block, obj="text", opacity=None):
    color = TailwindColors(block.get("color"))
    return color.display(obj, block.get("lightness"), opacity)
