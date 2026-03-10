from wagtail.embeds.oembed_providers import all_providers

heyzine = {
    "endpoint": "https://heyzine.com/api1/oembed",
    "urls": [r"^https?://(?:[-\w]+\.)?heyzine\.com/flip-book/.+$"],
}

EMBEDS_FINDERS = [
    {
        "class": "apps.base.embeds.finders.CustomOEmbedFinder",
        "providers": [*all_providers, heyzine],
    },
]
