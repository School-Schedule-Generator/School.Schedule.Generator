from django import forms
from django.forms import ModelForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 't', 'id': 'login', 'name': 'login',
                                                                         'placeholder': 'username or mail'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 't', 'id': 'password', 'name': 'password',
                                                                    'placeholder': 'password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        ogg = User.objects.filter(
            Q(email=username) | Q(username=username)
        ).first()

        if ogg and password:
            self.user_cache = authenticate(username=ogg.username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError('Invalid login or password.')
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput({'class': 't', 'id': 'username', 'name': 'username',
                                                                 'placeholder': 'username'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 't', 'id': 'email', 'name': 'email',
                                                                      'placeholder': 'email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 't', 'id': 'password',
                                                                            'name': 'password',
                                                                            'placeholder': 'password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 't', 'id': 'repeat-password',
                                                                            'name': 'repeat-password',
                                                                            'placeholder': 'repeat password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ScheduleListForm(ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 't', 'id': 'name', 'name': 'name',
                                                                   'placeholder': 'name'}))
    description = forms.CharField(label='', required=False, widget=forms.Textarea(attrs={
        'class': 't', 'id': 'description', 'name': 'description',
        'placeholder': 'description of your schedule(not required)'}))

    class Meta:
        model = ScheduleList
        fields = ['name', 'description']


class LessonHoursForm(ModelForm):
    start_hour = forms.TimeField(label='', widget=forms.TimeInput(attrs={
        'class': 't',
        'id': 'start-hour',
        'name': 'start-hour',
        'placeholder': 'start hour'
    }))

    class Meta:
        model = LessonHours
        fields = ['start_hour']


class ClassroomTypesForm(ModelForm):
    description = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 't',
        'id': 'classroom-type',
        'name': 'classroom-type',
        'placeholder': 'classroom type'
    }))

    class Meta:
        model = ClassroomTypes
        fields = ['description']


class ClassroomsForm(ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 't',
        'id': 'name',
        'name': 'name',
        'placeholder': 'classroom name'
    }))

    class Meta:
        model = Classrooms
        fields = ['name']


class TeachersForm(ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 't',
        'id': 'name',
        'name': 'name',
        'placeholder': 'name'
    }))

    surname = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 't',
        'id': 'surname',
        'name': 'surname',
        'placeholder': 'surname'
    }))

    class Meta:
        model = Teachers
        fields = ['name', 'surname']


class ClassesForm(ModelForm):
    grade = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'class': 't',
        'id': 'grade',
        'name': 'grade',
        'placeholder': 'grade'
    }))
    class_signature = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 't',
        'id': 'class-signature',
        'name': 'class-signature',
        'placeholder': 'class signature'
    }))

    class Meta:
        model = Classes
        fields = ['grade', 'class_signature']


class SubjectNamesForm(ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 't',
        'id': 'name',
        'name': 'name',
        'placeholder': 'subject name'
    }))
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


class SubjectsForm(ModelForm):
    subject_count_in_week = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'class': 't',
        'id': 'subject-count-in_week',
        'name': 'subject-count-in-week',
        'placeholder': 'subject-count-in-week'
    }))

    number_of_groups = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'class': 't',
        'id': 'number-of-groups',
        'name': 'number-of-groups',
        'placeholder': 'number-of-groups'
    }))

    max_stack = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'class': 't',
        'id': 'max-stack',
        'name': 'max-stack',
        'placeholder': 'max-stack'
    }))

    class Meta:
        model = Subject
        fields = ['subject_count_in_week', 'number_of_groups', 'max_stack']
