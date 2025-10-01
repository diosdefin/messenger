from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from chat.sitemaps import StaticViewSitemap, UserSitemap
from django.conf import settings
from django.conf.urls.static import static


sitemaps = {
    'static': StaticViewSitemap,
    'users': UserSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)