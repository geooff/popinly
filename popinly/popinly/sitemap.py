from django.urls import reverse
from django.contrib.sitemaps import Sitemap


class ViewSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""

    def items(self):
        # Return list of url names for views to include in sitemap
        return ["index", "register"]

    def location(self, item):
        return reverse(item)


sitemaps = {"views": ViewSitemap}
