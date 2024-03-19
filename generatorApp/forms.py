from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import *

# na razie formularze w ten sposob, jak bedzie to sie pozmienia w zaleznosci od potrzeb


class LoginForm(AuthenticationForm):
    username_or_email = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 't', 'id': 'login', 'name': 'login',
                                                                         'placeholder': 'username or mail'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 't', 'id': 'password', 'name': 'password',
                                                                    'placeholder': 'password'}))

# nie wiem czy logowanie przez maila bedzie dzialac
    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')
        user = None

        if username_or_email and password:
            if '@' in username_or_email:
                try:
                    user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    user = None
            else:
                user = authenticate(username=username_or_email, password=password)

        if user is None:
            raise forms.ValidationError('Invalid username/email or password.')
        elif not user.check_password(password):
            raise forms.ValidationError('Invalid username/email or password.')
        elif user.is_active:
            raise forms.ValidationError('This user is active.')
        else:
            self.user_cache = user

        return self.cleaned_data


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user


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
