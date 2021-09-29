from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from authapp.models import User
from basket.models import Basket
from geekshop import settings


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
            user = form.save()
            if send_verify_link(user):
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


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
        # 'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'authapp/profile.html', context)


def send_verify_link(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = f'для активации учетной записи {user.username} пройдите по ссылке'
    message = f'для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request,email,activation_key):

    user = User.objects.get(email=email)
    try:
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key=''
            user.activation_key_expires = None
            user.is_active = True
            user.save()
            auth.login(request,user)
        return render(request,'authapp/verification.html')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
