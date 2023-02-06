from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from scraping.models import *
__all__ = [
    'UserLogniForm',
    'UserRegistrationForm',
    'UserUpdateForm',
    'ContactForm',
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
            if not user.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, user.first().password):
                raise forms.ValidationError('Не верный пароль!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключен.')
        return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Введите email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Введите пароль')
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Введите пароль еще раз')

    class Meta:
        model = User
        fields = (
            'email',
        )

    def clean_password_2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password_2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=True, widget=forms.Select(attrs={'class': 'form-control'}), label='Город:')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=True, widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность')
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Получать рассылку')

    class Meta:
        model = User
        fields = (
            'city',
            'language'
            'send_email'
        )


class ContactForm(forms.Form):
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Город:')
    language = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Специальность')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Введите email')
