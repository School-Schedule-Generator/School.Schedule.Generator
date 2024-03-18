from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

# na razie formularze w ten sposob, jak bedzie to sie pozmienia w zaleznosci od potrzeb


class LoginForm(ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'repeat_password']


class ScheduleListForm(ModelForm):
    class Meta:
        model = ScheduleList
        fields = ['name']


class ClassroomTypesForm(ModelForm):
    class Meta:
        model = ClassroomTypes
        fields = ['description']


class ClassroomsForm(ModelForm):
    class Meta:
        model = Classrooms
        fields = ['name', 'type_id']


class TeachersForm(ModelForm):
    class Meta:
        model = Teachers
        fields = ['name', 'surname', 'main_classroom_id', 'possible_subjects',
                  'start_hour_index', 'end_hour_index', 'days']


class LessonHoursForm(ModelForm):
    class Meta:
        model = LessonHours
        fields = ['start_hour', 'duration']


class ClassesForm(ModelForm):
    class Meta:
        model = Classes
        fields = ['grade', 'class_signature', 'supervising_teacher_id', 'starting_lesson_hour_id']


class SubjectNamesForm(ModelForm):
    class Meta:
        model = SubjectNames
        fields = ['name']


class ScheduleSettingsForm(forms.Form):
    choices = (
        ('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'),
    )

    min_lessons_per_day = forms.IntegerField(label='min_lessons_per_day')
    max_lessons_per_day = forms.IntegerField(label='max_lessons_per_day')
    days = forms.MultipleChoiceField(label='days', choices=choices)


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['classes_id', 'subject_name_id', 'lesson_hour_id', 'teachers_id', 'classroom_id',
                  'subject_count_in_week', 'number_of_groups', 'max_stack', 'classroom_types']
