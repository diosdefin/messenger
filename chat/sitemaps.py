from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.contrib.auth.models import User

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['login', 'register', 'user_list', 'about_me']  # ДОБАВЬТЕ 'about_me'

    def location(self, item):
        return reverse(item)

class UserSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return User.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('chat', args=[obj.id])
    


