import sqlite3

import pandas as pd

from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .schoolSchedule.settings import settings


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


# add data from uploaded file to database
def upload_files(file_name, file, schedule_id):
    if file_name == 'classes':
        for index, row in file.itterows():
            data = Classes(
                schedule_id=schedule_id,
                supervising_teacher_id=row['supervising_teacher'],
                starting_lesson_hour_id=row['starting_lesson_hour_id'],
                grade=row['grade'],
                class_signature=row['class_signature']
            )
    elif file_name == 'classroom_types':
        pass
    elif file_name == 'classrooms':
        pass
    elif file_name == 'lesson_hours':
        pass
    elif file_name == 'subject_names':
        pass
    elif file_name == 'teachers':
        pass
    elif file_name == 'subjects':
        pass
    else:
        return False
    return True


def upload(request, schedule_id=None, file_name=None):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        # fs.save(file.name, file)

        allowed_extension = ['xlsx', 'ods']
        file_extension = file.name.split('.')[1]

        if file_extension not in allowed_extension:
            messages.error(request, 'Wrong file type')
            return render(request, 'generatorApp/test.html', context={})

        if file_extension == 'ods':
            df = pd.read_excel(file.name, engine="odf")
        else:
            df = pd.read_excel(file.name)

        if not upload_files(file_name, df, schedule_id):
            messages.error(request, 'Wrong file name')
            return render(request, 'generatorApp/test.html', context={})

        return render(request, 'generatorApp/test.html', context={})

    return render(request, 'generatorApp/test.html')
