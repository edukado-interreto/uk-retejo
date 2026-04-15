from django import template
from wagtail.models import Page

register = template.Library()


@register.simple_tag(takes_context=True)
def if_current(context, page, css_class):
    request = context["request"]
    return css_class if request.path == page.get_url(request) else ""


@register.filter
def ancestors(page):
    return [p for p in page.get_ancestors() if not p.is_root()]
