from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from chat.sitemaps import StaticViewSitemap, UserSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'users': UserSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]