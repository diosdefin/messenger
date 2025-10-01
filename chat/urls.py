from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.user_list, name='user_list'),
    path('chat/<int:user_id>/', views.chat, name='chat'),
    path('api/chat/<int:user_id>/messages/', views.get_new_messages, name='get_messages'),
    path('api/chat/<int:user_id>/send_sticker/', views.send_sticker, name='send_sticker'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('about/', views.about_me, name='about_me'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)