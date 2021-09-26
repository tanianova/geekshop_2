from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from authapp.forms import UserLoginForm, UserRegisterForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}

    return render(request, 'authapp/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('auth:login'))

    else:
        form = UserRegisterForm()
    context = {
        'title': 'GeekShop - Регистрация',
        'form': form,
    }
    return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))