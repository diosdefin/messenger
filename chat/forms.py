from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля более красивыми
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Придумайте логин'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Придумайте пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторите пароль'})

class MessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Введите ваше сообщение...',
            'class': 'form-control'
        }),
        max_length=1000
    )