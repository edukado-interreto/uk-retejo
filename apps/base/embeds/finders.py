from wagtail.embeds.finders.oembed import OEmbedFinder


class CustomOEmbedFinder(OEmbedFinder):
    def find_embed(self, url, max_width=None, max_height=None):
        result = super().find_embed(url, max_width, max_height)
        if result["title"] is None:
            result["title"] = ""
        return result
