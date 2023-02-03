from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
__all__ = [
    'UserLogniForm',
]


User = get_user_model()


class UserLogniForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = User.objects.filter(email=email)
            print(user)
            if not user.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, user.first().password):
                raise forms.ValidationError('Не верный пароль!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключен.')
        return super().clean(*args, **kwargs)
