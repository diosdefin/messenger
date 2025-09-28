from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # ✅ ДОБАВЬ ЭТУ СТРОЧКУ!

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.user_list, name='user_list'),
    path('chat/<int:user_id>/', views.chat, name='chat'),
    path('api/chat/<int:user_id>/messages/', views.get_new_messages, name='get_messages'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]
