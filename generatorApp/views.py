import pandas as pd
from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
# from .schoolSchedule.settings import settings


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

        user = User.objects.create_user(
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
def upload_file(file_name, file, schedule_id):
    if file_name == 'classes':
        for index, row in file.itterows():
            _, grade, class_signature, supervising_teacher, starting_lesson_hour_id = row.values
            data = Classes.objects.create(
                schedule_id=schedule_id,
                supervising_teacher_id=supervising_teacher,
                starting_lesson_hour_id=starting_lesson_hour_id,
                grade=grade,
                class_signature=class_signature
            )
            data.save()
    elif file_name == 'classroom_types':
        for index, row in file.itterows():
            _, description = row.values
            data = ClassroomTypes.objects.create(schedule_id=schedule_id, description=description)
            data.save()
    elif file_name == 'classrooms':
        for index, row in file.itterows():
            _, name, type_id = row.values
            data = Classrooms.objects.create(schedule_id=schedule_id, name=name, type_id=type_id)
            data.save()
    elif file_name == 'lesson_hours':
        for index, row in file.itterows():
            _, start_hour, duration = row.values
            data = LessonHours.objects.create(schedule_id=schedule_id, start_hour=start_hour, duration=duration)
            data.save()
    elif file_name == 'subject_names':
        for index, row in file.itterows():
            _, name = row.values
            data = SubjectNames.objects.create(schedule_id=schedule_id, name=name)
            data.save()
    elif file_name == 'teachers':
        for index, row in file.itterows():
            _, main_classroom_id, name, surname, possible_subjects, start_hour_index, end_hour_index, days = row.values
            data = Teachers.objects.create(
                schedule_id=schedule_id,
                main_classroom_id=main_classroom_id,
                name=name,
                surname=surname,
                possible_subjects=possible_subjects,
                start_hour_index=start_hour_index,
                end_hour_index=end_hour_index,
                days=days
            )
            data.save()
    elif file_name == 'subjects':
        for index, row in file.itterows():
            _, subject_name_id, teacher_id, lesson_hour_id, classroom_id, subject_count_in_week, number_of_groups, max_stack, classroom_types = row.values
            data = Subject.objects.create(
                schedule_id=schedule_id,
                subject_name_id=subject_name_id,
                teacher_id=teacher_id,
                lesson_hour_id=lesson_hour_id,
                classroom_id=classroom_id,
                subject_count_in_week=subject_count_in_week,
                number_of_groups=number_of_groups,
                max_stack=max_stack,
                classroom_types=classroom_types
            )
            data.save()
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

        if not upload_file(file_name, df, schedule_id):
            messages.error(request, 'Wrong file name.')
            return render(request, 'generatorApp/test.html', context={})

        return render(request, 'generatorApp/test.html', context={})

    return render(request, 'generatorApp/test.html')
