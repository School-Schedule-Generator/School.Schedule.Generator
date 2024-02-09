from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_register(request):
    if request.user.is_authenticated:
        messages.success(request, f'You are logged as {request.user.username}')
        return HttpResponseRedirect(reverse('generatorApp:home'))

    return render(request, 'generatorApp/login_register.html', {})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, f'You are logged as {user.username}')
            return HttpResponseRedirect(reverse('generatorApp:home'))
        else:
            messages.error(request, 'Login failed. Please check your username and password.')
            return HttpResponseRedirect(reverse('generatorApp:login_register'))

    return HttpResponseRedirect(reverse('generatorApp:login_register'))


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat-password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is taken. Please choice different one.')
            return HttpResponseRedirect(reverse('generatorApp:login_register'))

        if password != repeat_password:
            messages.error(request, 'Passwords must be identical!')
            return HttpResponseRedirect(reverse('generatorApp:login_register'))

        user = User(
            username=username,
            password=password
        )
        user.save()

        login(request, user)

        messages.success(request, f'You are logged as {user.username}')
        return HttpResponseRedirect(reverse('generatorApp:home'))

    return HttpResponseRedirect(reverse('generatorApp:login_register'))


def home(request):
    return render(request, 'generatorApp/home.html')
