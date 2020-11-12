from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    # Returns the QuerySet of objects to include in the sitemap
    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
