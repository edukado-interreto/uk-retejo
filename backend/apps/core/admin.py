from django.contrib import admin
from wagtail.embeds.models import Embed

from apps.base.models import FontAwesomeIcon

admin.site.register(Embed)
admin.site.register(FontAwesomeIcon)
