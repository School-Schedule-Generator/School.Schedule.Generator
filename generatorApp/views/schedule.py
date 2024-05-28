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
        sort_by = self.request.GET.get('sort_by')
        if sort_by in [field.name for field in ScheduleList._meta.get_fields()]:
            context['schedule_list'] = ScheduleList.objects.filter(user_id=self.request.user).order_by(sort_by)
        else:
            context['schedule_list'] = ScheduleList.objects.filter(user_id=self.request.user)
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

                            print(subject['classroom_id'])
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
        schedule_name = context['schedule_name']
        schedule = ScheduleList.objects.get(user_id=self.request.user, name=schedule_name)
        context['schedule'] = schedule

        sort_by = self.request.GET.get('sort_by')
        if sort_by in [field.name for field in ScheduleList._meta.get_fields()]:
            context['schedule_list'] = ScheduleList.objects.filter(user_id=self.request.user).order_by(sort_by)
        else:
            context['schedule_list'] = ScheduleList.objects.filter(user_id=self.request.user)
        context['labels'] = [
            'lesson_hours',
            'classroom_types',
            'classrooms',
            'teachers',
            'classes',
            'subject_names',
            'subjects'
        ]

        schedule_str = schedule_str(schedule)
        context['schedule_content'] = schedule_str if schedule_str else "Please import data!"

        return context


class LessonHoursView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('generatorApp:login')
    form_class = LessonHoursForm
    template_name = 'generatorApp/forms/lesson_hours.html'
    # success_url = reverse_lazy('generatorApp:schedules_base')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get('sort_by')
        if sort_by in [field.name for field in ScheduleList._meta.get_fields()]:
            context['schedule_list'] = ScheduleList.objects.filter(user_id=self.request.user).order_by(sort_by)
        else:
            context['schedule_list'] = ScheduleList.objects.filter(user_id=self.request.user)
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


def upload_file(file_name, file, schedule_id):
    schedule = ScheduleList.objects.get(id=schedule_id)
    try:
        if file_name == 'classes':
            for index, row in file.iterrows():
                _id, grade, class_signature, supervising_teacher, starting_lesson_hour_id = row.values

                if not Classes.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        supervising_teacher_id=Teachers.objects.get(_id=supervising_teacher, schedule_id=schedule),
                        starting_lesson_hour_id=LessonHours.objects.get(_id=starting_lesson_hour_id,
                                                                        schedule_id=schedule),
                        grade=grade,
                        class_signature=class_signature
                ).exists():
                    data = Classes.objects.create(
                        _id=_id,
                        schedule_id=schedule,
                        supervising_teacher_id=Teachers.objects.get(_id=supervising_teacher, schedule_id=schedule),
                        starting_lesson_hour_id=LessonHours.objects.get(_id=starting_lesson_hour_id,
                                                                        schedule_id=schedule),
                        grade=grade,
                        class_signature=class_signature
                    )
                    data.save()

        elif file_name == 'classroom_types':
            for index, row in file.iterrows():
                _id, description = row.values
                if not ClassroomTypes.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        description=description
                ).exists():
                    data = ClassroomTypes.objects.create(_id=_id, schedule_id=schedule, description=description)
                    data.save()
        elif file_name == 'classrooms':
            for index, row in file.iterrows():
                _id, name, type_id = row.values
                if not Classrooms.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        name=name,
                        type_id=ClassroomTypes.objects.get(id=type_id, schedule_id=schedule)
                ).exists():
                    data = Classrooms.objects.create(_id=_id, schedule_id=schedule, name=name,
                                                     type_id=ClassroomTypes.objects.get(id=type_id))
                    data.save()
        elif file_name == 'lesson_hours':
            for index, row in file.iterrows():
                _id, start_hour, duration = row.values
                if not LessonHours.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        start_hour=start_hour,
                        duration=duration
                ).exists():
                    data = LessonHours.objects.create(
                        _id=_id,
                        schedule_id=schedule,
                        start_hour=start_hour,
                        duration=duration
                    )
                    data.save()
        elif file_name == 'subject_names':
            for index, row in file.iterrows():
                _id, name = row.values
                if not SubjectNames.objects.filter(_id=_id, schedule_id=schedule, name=name).exists():
                    data = SubjectNames.objects.create(_id=_id, schedule_id=schedule, name=name)
                    data.save()
        elif file_name == 'teachers':
            for index, row in file.iterrows():
                _id, name, surname, possible_subjects, start_hour_index, end_hour_index, days, main_classroom_id = row.values
                if not Teachers.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        main_classroom_id=Classrooms.objects.get(_id=main_classroom_id,
                                                                 schedule_id=schedule) if main_classroom_id != 'Null' else None,
                        end_hour_index=end_hour_index,
                        days=days
                ).exists():
                    data = Teachers.objects.create(
                        _id=_id,
                        schedule_id=schedule,
                        main_classroom_id=Classrooms.objects.get(_id=main_classroom_id,
                                                                 schedule_id=schedule) if main_classroom_id != 'Null' else None,
                        name=name,
                        surname=surname,
                        possible_subjects=possible_subjects,
                        start_hour_index=start_hour_index,
                        end_hour_index=end_hour_index,
                        days=days
                    )
                    data.save()
        elif file_name == 'subjects':
            for index, row in file.iterrows():
                (
                    _id,
                    subject_name_id,
                    classes_id,
                    subject_count_in_week,
                    number_of_groups,
                    lesson_hour_id,
                    teachers_id,
                    classroom_id,
                    max_stack,
                    classroom_types
                ) = row.values

                if not Subject.objects.filter(
                        _id=_id,
                        schedule_id=schedule,
                        classes_id=Classes.objects.get(_id=classes_id, schedule_id=schedule),
                        subject_name_id=SubjectNames.objects.get(_id=subject_name_id, schedule_id=schedule),
                        lesson_hour_id=LessonHours.objects.get(_id=lesson_hour_id, schedule_id=schedule) if str(
                            lesson_hour_id) != 'nan' else None,
                        teachers_id=teachers_id,
                        classroom_id=Classrooms.objects.get(_id=classroom_id, schedule_id=schedule) if str(
                            classroom_id) != 'nan' else None,
                        subject_count_in_week=subject_count_in_week,
                        number_of_groups=number_of_groups,
                        max_stack=max_stack,
                        classroom_types=classroom_types
                ).exists():
                    data = Subject.objects.create(
                        _id=_id,
                        schedule_id=schedule,
                        classes_id=Classes.objects.get(_id=classes_id, schedule_id=schedule),
                        subject_name_id=SubjectNames.objects.get(_id=subject_name_id, schedule_id=schedule),
                        lesson_hour_id=LessonHours.objects.get(_id=lesson_hour_id, schedule_id=schedule) if str(
                            lesson_hour_id) != 'nan' else None,
                        teachers_id=teachers_id,
                        classroom_id=Classrooms.objects.get(_id=classroom_id, schedule_id=schedule) if str(
                            classroom_id) != 'nan' else None,
                        subject_count_in_week=subject_count_in_week,
                        number_of_groups=number_of_groups,
                        max_stack=max_stack,
                        classroom_types=classroom_types
                    )
                    if data.check_teachers(teachers_id, schedule):
                        data.save()
        else:
            return False
    except ValueError:
        return False
    return True


def get_upload_file(request, file_name=None, schedule_id=None):
    if request.method == 'POST' and request.FILES['file']:
        file_names = [
            'lesson_hours',
            'classroom_types',
            'classrooms',
            'teachers',
            'classes',
            'subject_names',
            'subjects'
        ]
        try:
            next_file = file_names[file_names.index(file_name) + 1]
        except IndexError:
            next_file = False

        file = request.FILES['file']
        fs = FileSystemStorage()
        fs.save(file.name, file)

        allowed_extension = ['xlsx', 'ods']
        file_extension = file.name.split('.')[1]

        if file_extension not in allowed_extension:
            fs.delete(file.name)
            messages.error(request, 'Wrong file type')
            return render(request, 'generatorApp/forms/upload.html', context={})

        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        if file_extension == 'ods':
            df = pd.read_excel(file_path, engine="odf")
        else:
            df = pd.read_excel(file_path)

        fs.delete(file.name)
        if not upload_file(file_name, df, schedule_id):
            messages.error(request,
                           f'Wrong file name or format. Pass in {file_name} again. For help see documentation.')
            return HttpResponseRedirect(
                reverse('generatorApp:get-upload-file', kwargs={'file_name': file_name, 'schedule_id': schedule_id})
            )
        if next_file:
            return HttpResponseRedirect(
                reverse('generatorApp:get-upload-file', kwargs={'file_name': next_file, 'schedule_id': schedule_id})
            )
        else:
            return HttpResponseRedirect(reverse('generatorApp:settings', kwargs={'schedule_id': schedule_id}))

    return render(request, 'generatorApp/forms/upload.html', context={'file_name': file_name})


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