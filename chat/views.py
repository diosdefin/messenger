from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.db import models
from django.contrib import messages as django_messages
from .models import Message
from .forms import CustomUserCreationForm, MessageForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_list')
    return render(request, 'chat/login.html')

@login_required
def user_list(request):
    # Показываем только активных пользователей
    users = User.objects.exclude(id=request.user.id).filter(is_active=True)
    unread_counts = {}
    for user in users:
        unread_counts[user.id] = Message.get_unread_count(request.user, user)
    return render(request, 'chat/user_list.html', {
        'users': users,
        'unread_counts': unread_counts
    })

@login_required
def chat(request, user_id):
    # Проверяем, что пользователь активен
    receiver = get_object_or_404(User, id=user_id, is_active=True)
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=receiver) |
        models.Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    # Помечаем сообщения как прочитанные
    Message.objects.filter(sender=receiver, receiver=request.user, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=form.cleaned_data['content']
            )
            return redirect('chat', user_id=user_id)
    else:
        form = MessageForm()
    
    return render(request, 'chat/chat.html', {
        'receiver': receiver,
        'messages': messages,
        'form': form
    })

# Добавим JSON API для проверки новых сообщений
@login_required
def get_new_messages(request, user_id):
    receiver = get_object_or_404(User, id=user_id, is_active=True)
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=receiver) |
        models.Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')
    
    messages_data = []
    for message in messages:
        messages_data.append({
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%H:%M'),
            'is_sent': message.sender == request.user
        })
    
    return JsonResponse({'messages': messages_data})

# Функция удаления пользователя
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Выходим из системы
        logout(request)
        # Удаляем все сообщения пользователя
        Message.objects.filter(sender=user).delete()
        Message.objects.filter(receiver=user).delete()
        # Удаляем самого пользователя
        user.delete()
        django_messages.success(request, 'Ваш аккаунт был успешно удалён')
        return redirect('login')
    
    return render(request, 'chat/delete_account.html')

# Функция для удаления другого пользователя (только для админов)
@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет прав для этого действия")
    
    user_to_delete = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Удаляем все сообщения пользователя
        Message.objects.filter(sender=user_to_delete).delete()
        Message.objects.filter(receiver=user_to_delete).delete()
        # Удаляем пользователя
        user_to_delete.delete()
        django_messages.success(request, f'Пользователь {user_to_delete.username} был удалён')
        return redirect('user_list')
    
    return render(request, 'chat/confirm_delete.html', {'user_to_delete': user_to_delete})