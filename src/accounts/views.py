from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import *
__all__ = [
    'login_view',
    'logout_view',
]


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
