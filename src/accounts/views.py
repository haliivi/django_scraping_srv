from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, render
from .forms import *
from scraping.models import *
from django.contrib import messages
import datetime as dt
__all__ = [
    'login_view',
    'logout_view',
    'register_view',
    'update_view',
    'delete_view',
    'contact',
]


User = get_user_model()


def login_view(request):
    form = UserLogniForm(request.POST or None)
    if form.is_valid():
        data = form.clean()
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему.')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные сохранены.')
                return redirect('accounts:update')
        form = UserUpdateForm(initial={
            'city': user.city,
            'language': user.language,
            'send_email': user.send_email,
        })
        return render(request, 'accounts/update.html', {'form': form, 'contact_form': contact_form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            User.objects.get(pk=user.pk).delete()
            messages.error(request, 'Пользователь удален!!!')
    return redirect('home')


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.clined_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'language': language, 'email': email})
                err.data['user_data'] = data
                err.save()
            else:
                data = [{'city': city, 'language': language, 'email': email}]
                Error(data=f'user_data:{data}').save()
            messages.success(request, 'Данные отправлены администрации.')
            return redirect(request, 'accounts:update')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')
