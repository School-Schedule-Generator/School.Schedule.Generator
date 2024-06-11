import os
import datetime as dt
from datetime import datetime
import pandas as pd
from django.shortcuts import render, HttpResponseRedirect
from ..forms import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, ListView, CreateView
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import redirect
from ..schoolSchedule.load_data import load_data, schedule_to_json
from ..schoolSchedule.generate import generate_schedule
from django.core.exceptions import ValidationError
from .upload_file import upload_file


def update_context(request, kwargs, context):
    context['schedule_name'] = kwargs.get('schedule_name')
    sort_by = request.GET.get('sort_by')
    if sort_by in [field.name for field in ScheduleList._meta.get_fields()]:
        context['schedule_list'] = ScheduleList.objects.filter(user_id=request.user).order_by(sort_by)
    else:
        context['schedule_list'] = ScheduleList.objects.filter(user_id=request.user)
    context['labels'] = [
        'lesson_hours',
        'classroom_types',
        'classrooms',
        'teachers',
        'classes',
        'subject_names',
        'subjects'
    ]
    return context


class SchedulesListView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('generatorApp:login')
    form_class = ScheduleListForm
    template_name = 'generatorApp/schedules.html'
    success_url = reverse_lazy('generatorApp:schedules_base')

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        description = form.cleaned_data.get('description')

        username = self.request.user.username
        self.success_url += f'{username}/{name}'

        if ScheduleList.objects.filter(user_id=self.request.user, name=name).exists():
            raise ValidationError('Schedule with this name exist')

        schedule = ScheduleList.objects.create(
            user_id=self.request.user,
            name=name,
            description=description,
            content=''
        )
        schedule.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = update_context(self.request, self.kwargs, context)
        return context


class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'generatorApp/schedule.html'

    def get_context_data(self, **kwargs):
        def schedule_str(schedule):
            if not schedule.content:
                return False
            schedule_content = json.loads(schedule.content)
            for class_id, days in schedule_content.items():
                for day, subjects in days.items():
                    for subject_list in subjects:
                        for subject in subject_list:
                            subject_name = schedule.subjectnames_set.filter(_id=subject['subject_name_id']).first()
                            subject['subject_name_id'] = subject_name.name if subject_name else '---'

                            teacher_names = []
                            for teacher in subject['teachers_id']:
                                teacher = schedule.teachers_set.filter(_id=teacher).first()
                                teacher_names.append(f'{teacher.name} {teacher.surname}' if teacher else '--- ---')
                            subject['teachers_id'] = teacher_names[-1]

                            classroom = schedule.classrooms_set.filter(_id=subject['classroom_id']).first()
                            subject['classroom_id'] = classroom.name if classroom else '---'

                            lesson_hour = schedule.lessonhours_set.filter(_id=subject['lesson_hour_id']).first()
                            if lesson_hour:
                                start_hour = datetime.strptime(lesson_hour.start_hour, '%H:%M:%S')
                                end_hour = (start_hour + dt.timedelta(minutes=45))

                                subject['lesson_hour_id'] = f'{start_hour.strftime("%H:%M")}-{end_hour.strftime("%H:%M")}'
                            else:
                                subject['lesson_hour_id'] = '---'

            return schedule_content

        context = super().get_context_data(**kwargs)
        context = update_context(self.request, self.kwargs, context)
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)
        context['schedule'] = schedule

        schedule_str = schedule_str(schedule)
        context['schedule_content'] = schedule_str if schedule_str else "Please import data!"

        return context


class LessonHoursView(LoginRequiredMixin, TemplateView, FormView):
    login_url = reverse_lazy('generatorApp:login')
    form_class = LessonHoursForm
    template_name = 'generatorApp/forms/lesson_hours.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        context = update_context(self.request, self.kwargs, context)
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)
        context['objects_list'] = LessonHours.objects.filter(schedule_id=schedule).all()
        return context

    def form_valid(self, form, **kwargs):
        # TODO-validation: check if start hour is bigger then last one (prevent indexing bug when generating)
        context = self.get_context_data()
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)
        start_hour = form.cleaned_data.get('start_hour')

        last_obj = context['objects_list'].last()

        LessonHours.objects.create(
            _id=int(last_obj._id)+1 if last_obj else 0,
            schedule_id=schedule,
            start_hour=start_hour,
            duration=45
        )
        return redirect(self.request.build_absolute_uri())


class ClassroomTypesView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('generatorApp:login')
    form_class = ClassroomTypesForm
    template_name = 'generatorApp/forms/classroom_types.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = update_context(self.request, self.kwargs, context)
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)
        context['objects_list'] = ClassroomTypes.objects.filter(schedule_id=schedule).all()
        return context

    def form_valid(self, form, **kwargs):
        context = self.get_context_data()
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)

        description = form.cleaned_data.get('description')

        last_obj = context['objects_list'].last()

        ClassroomTypes.objects.create(
            _id=int(last_obj._id)+1 if last_obj else 0,
            schedule_id=schedule,
            description=description,
        )
        return redirect(self.request.build_absolute_uri())


class ClassroomsView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('generatorApp:login')
    form_class = ClassroomsForm
    template_name = 'generatorApp/forms/classrooms.html'
    # success_url = reverse_lazy('generatorApp:schedules_base')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = update_context(self.request, self.kwargs, context)
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)
        context['objects_list'] = Classrooms.objects.filter(schedule_id=schedule).all()
        context['queryset'] = ClassroomTypes.objects.filter(schedule_id=schedule)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)

        name = form.cleaned_data.get('name')
        type_id_desc = self.request.POST.get('type-id')

        #TODO: walidacja - wartosci w description nie moga sie powtarzac, musza byc unikalne
        type_id = ClassroomTypes.objects.filter(schedule_id=schedule, description=type_id_desc).first()
        print('a'*50)
        print(type_id)

        last_obj = context['objects_list'].last()

        Classrooms.objects.create(
            _id=int(last_obj._id) + 1 if last_obj else 0,
            schedule_id=schedule,
            type_id=type_id,
            name=name
        )
        return redirect(self.request.build_absolute_uri())


class TeachersView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('generatorApp:login')
    form_class = TeachersForm
    template_name = 'generatorApp/forms/teachers.html'
    # success_url = reverse_lazy('generatorApp:schedules_base')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = update_context(self.request, self.kwargs, context)
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)
        context['objects_list'] = Teachers.objects.filter(schedule_id=schedule).all()

        # listy elemntow do selektow
        context['classrooms_queryset'] = Classrooms.objects.filter(schedule_id=schedule)
        context['subjects_queryset'] = SubjectNames.objects.filter(schedule_id=schedule)
        context['lesson_hours_queryset'] = LessonHours.objects.filter(schedule_id=schedule)
        return context

    def form_valid(self, form):
        #TODO: dokonczyc pobieranie elementow z formularzy
        context = self.get_context_data()
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)

        name = form.cleaned_data.get('name')
        surname = form.cleaned_data.get('name')
        type_id_desc = self.request.POST.get('type-id')

        # TODO: walidacja - wartosci w description nie moga sie powtarzac, musza byc unikalne
        type_id = ClassroomTypes.objects.filter(schedule_id=schedule, description=type_id_desc).first()
        print('a' * 50)
        print(type_id)

        last_obj = context['objects_list'].last()

        Teachers.objects.create(
            _id=int(last_obj._id) + 1 if last_obj else 0,
            schedule_id=schedule,
            name=name,
            surname=surname
        )
        return redirect(self.request.build_absolute_uri())


class ClassesView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('generatorApp:login')
    form_class = ClassesForm
    template_name = 'generatorApp/forms/classes.html'
    # success_url = reverse_lazy('generatorApp:schedules_base')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = update_context(self.request, self.kwargs, context)
        return context


class SubjectNamesView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('generatorApp:login')
    form_class = SubjectNamesForm
    template_name = 'generatorApp/forms/subject_names.html'
    # success_url = reverse_lazy('generatorApp:schedules_base')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = update_context(self.request, self.kwargs, context)
        return context


class SubjectsView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('generatorApp:login')
    form_class = SubjectsForm
    template_name = 'generatorApp/forms/subjects.html'
    # success_url = reverse_lazy('generatorApp:schedules_base')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = update_context(self.request, self.kwargs, context)
        return context


def get_upload_file(request, file_name=None, schedule_id=None):
    if request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        fs.save(file.name, file)

        allowed_extension = ['xlsx', 'ods']
        file_extension = file.name.split('.')[1]

        if file_extension not in allowed_extension:
            fs.delete(file.name)
            return False

        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        if file_extension == 'ods':
            df = pd.read_excel(file_path, engine="odf")
        else:
            df = pd.read_excel(file_path)

        fs.delete(file.name)
        return upload_file(file_name, df, schedule_id)


def create_schedule(request):
    if request.method == 'POST':
        schedule = ScheduleList.objects.create(
            user_id=request.user,
            name=request.POST.get('name'),
        )
        schedule.save()
        ScheduleSettings.objects.create(schedule_id=schedule)
        return redirect(f'/upload/{schedule.id}')

    return render(request, 'generatorApp/create_schedule.html')


def upload(request, schedule_id=None):
    if schedule_id is None:
        return render(request, 'generatorApp/create_schedule.html')

    return redirect(f'/upload/lesson_hours/{schedule_id}')


def schedule_settings(request, schedule_id=None):
    settings = ScheduleSettings.objects.get(schedule_id=schedule_id)

    if request.method == 'POST':
        min_lessons_per_day = request.POST.get("min_lessons_per_day")
        max_lessons_per_day = request.POST.get("max_lessons_per_day")
        settings.content = json.dumps({
            "min_lessons_per_day": int(min_lessons_per_day) if min_lessons_per_day is not None else 5,
            "max_lessons_per_day": int(max_lessons_per_day) if max_lessons_per_day is not None else 9,
            "days": request.POST.getlist("days")
        })
        settings.save()

        # prepare and generate data
        now = datetime.now()
        data = load_data(
            dtype='sql',
            schedule_id=schedule_id
        )
        if data:
            schedule_pd = generate_schedule(
                data=data,
                schedule_settings=json.loads(settings.content),
                log_file_name=now.strftime("%Y-%m-%d %H-%M-%S.%f")
            )

            schedule = ScheduleList.objects.get(id=schedule_id)
            schedule.content = schedule_to_json(schedule_pd, file_path=None)
            schedule.save()

    context = json.loads(settings.content)
    context.update({"schedule_id": schedule_id})

    return render(request, 'generatorApp/settings.html', context=context)
