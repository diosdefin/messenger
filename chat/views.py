from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.db import models
from django.contrib import messages as django_messages
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .models import Message
from .forms import CustomUserCreationForm, MessageForm

def get_seo_context():
    return {
        'site_name': 'ElChat - Современный мессенджер',
        'site_description': 'Бесплатный мессенджер для быстрого и безопасного общения',
        'default_title': 'ElChat - Мессенджер для общения',
        'default_description': 'Общайтесь бесплатно в нашем мессенджере',
    }

def register(request):
    seo_context = get_seo_context()
    context = {
        'meta_title': 'Регистрация в ElChat | Бесплатный мессенджер',
        'meta_description': 'Зарегистрируйтесь в ElChat - современном мессенджере для общения',
        **seo_context
    }
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            django_messages.success(request, 'Добро пожаловать в ElChat!')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    
    context['form'] = form
    return render(request, 'chat/register.html', context)

def login_view(request):
    seo_context = get_seo_context()
    context = {
        'meta_title': 'Вход в ElChat | Мессенджер для общения',
        'meta_description': 'Войдите в свой аккаунт ElChat для начала общения',
        **seo_context
    }
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_list')
        else:
            django_messages.error(request, 'Неверный логин или пароль')
    
    return render(request, 'chat/login.html', context)

@login_required
def user_list(request):
    seo_context = get_seo_context()
    users = User.objects.exclude(id=request.user.id).filter(is_active=True)
    
    unread_counts = {}
    for user in users:
        unread_counts[user.id] = Message.get_unread_count(request.user, user)
    
    context = {
        'meta_title': 'Пользователи ElChat | Список контактов',
        'meta_description': 'Список пользователей ElChat для начала общения',
        'users': users,
        'unread_counts': unread_counts,
        **seo_context
    }
    return render(request, 'chat/user_list.html', context)

def about_me(request):
    seo_context = get_seo_context()
    context = {
        'meta_title': 'О создателе ElChat | Современный мессенджер',
        'meta_description': 'ElChat - современный мессенджер для удобного общения',
        **seo_context
    }
    return render(request, 'chat/about_me.html', context)

@login_required
def chat(request, user_id):
    try:
        receiver = get_object_or_404(User, id=user_id, is_active=True)
        messages = Message.objects.filter(
            models.Q(sender=request.user, receiver=receiver) |
            models.Q(sender=receiver, receiver=request.user)
        ).order_by('timestamp')

        # Помечаем сообщения как прочитанные
        Message.objects.filter(sender=receiver, receiver=request.user, is_read=False).update(is_read=True)
        
        seo_context = get_seo_context()
        context = {
            'meta_title': f'Чат с {receiver.username} | ElChat Мессенджер',
            'meta_description': f'Чат с пользователем {receiver.username} в ElChat',
            'receiver': receiver,
            'messages': messages,
            **seo_context
        }
        
        if request.method == 'POST':
            message_type = request.POST.get('message_type', 'text')
            media_file = request.FILES.get('media_file')
            content = request.POST.get('content', '')
            
            # Создаем сообщение
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                message_type=message_type,
                media_file=media_file
            )
            return redirect('chat', user_id=user_id)
        else:
            form = MessageForm()
        
        context['form'] = form
        return render(request, 'chat/chat.html', context)
    
    except Exception as e:
        django_messages.error(request, f'Ошибка: {str(e)}')
        return redirect('user_list')

@login_required
def get_new_messages(request, user_id):
    try:
        receiver = get_object_or_404(User, id=user_id, is_active=True)
        messages = Message.objects.filter(
            models.Q(sender=request.user, receiver=receiver) |
            models.Q(sender=receiver, receiver=request.user)
        ).order_by('timestamp')
        
        messages_data = []
        for message in messages:
            messages_data.append({
                'id': message.id,
                'sender': message.sender.username,
                'content': message.content,
                'message_type': message.message_type,
                'media_url': message.media_file.url if message.media_file else None,
                'timestamp': message.timestamp.strftime('%H:%M'),
                'is_sent': message.sender == request.user,
            })
        
        return JsonResponse({'messages': messages_data})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@csrf_exempt
def send_sticker(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sticker = data.get('sticker', '')
            
            receiver = get_object_or_404(User, id=user_id)
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=sticker,
                message_type='sticker'
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        Message.objects.filter(sender=user).delete()
        Message.objects.filter(receiver=user).delete()
        user.delete()
        django_messages.success(request, 'Ваш аккаунт был успешно удалён')
        return redirect('login')
    
    return render(request, 'chat/delete_account.html')

@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет прав для этого действия")
    
    user_to_delete = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        Message.objects.filter(sender=user_to_delete).delete()
        Message.objects.filter(receiver=user_to_delete).delete()
        user_to_delete.delete()
        django_messages.success(request, f'Пользователь {user_to_delete.username} был удалён')
        return redirect('user_list')
    
    return render(request, 'chat/confirm_delete.html', {'user_to_delete': user_to_delete})






from django.shortcuts import render
from django.contrib.auth.models import User

def user_list(request):
    users = User.objects.all()

    # список смайлов как Python-массив
    stickers = [
        "😀","😃","😄","😁","😆","😅","😂","🤣","😊","😇",
        "🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚",
        "😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🤩",
        "🥳","😏","😒","😞","😔","😟","😕","🙁","☹️","😣",
        "😖","😫","😩","🥺","😢","😭","😤","😠","😡","🤬",
        "🤯","😳","🥵","🥶","😱","😨","😰","😥","😓","🤗",
        "🤔","🤭","🤫","🤥","😶","😐","😑","😬","🙄","😯",
        "😦","😧","😮","😲","🥱","😴","🤤","😪","😵","🤐",
        "🥴","🤢","🤮","🤧","😷","🤒","🤕","🤑","🤠","😈",
        "👿","👹","👺","🤡","💩","👻","💀","☠️","👽","👾",
        "🤖","🎃","😺","😸","😹","😻","😼","😽","🙀","😿","😾"
    ]

    return render(request, "chat/user_list.html", {
        "users": users,
        "stickers": stickers
    })
