from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from .views import *

app_name = "generatorApp"
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    # accounts
    path('accounts/login/', views.LoginUserView.as_view(), name='login'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', views.LogoutUserView.as_view(), name='logout'),

    # docs
    path('docs/', lambda request: HttpResponseRedirect(reverse('generatorApp:docs', kwargs={'lang': 'eng', 'file': 'intro'})), name='redirect-docs'),
    path('docs/<str:lang>/<str:file>/', views.DocsView.as_view(), name='docs'),

    # schedules
    path('schedules/', views.SchedulesListView.as_view(), name='schedules_base'),
    path('schedules/<str:username>/', views.SchedulesListView.as_view(), name='schedules'),
    path('schedules/<str:username>/<str:schedule_name>/', views.ScheduleView.as_view(), name='schedule'),

    # forms to add data
    path('schedules/<str:username>/<str:schedule_name>/lesson_hours', views.LessonHoursView.as_view(), name='lesson_hours'),
    path('schedules/<str:username>/<str:schedule_name>/classroom_types', views.ClassroomTypesView.as_view(), name='classroom_types'),
    path('schedules/<str:username>/<str:schedule_name>/classrooms', views.ClassroomsView.as_view(), name='classroom'),
    path('schedules/<str:username>/<str:schedule_name>/teachers', views.TeachersView.as_view(), name='teachers'),
    path('schedules/<str:username>/<str:schedule_name>/classes', views.ClassesView.as_view(), name='classes'),
    path('schedules/<str:username>/<str:schedule_name>/subject_names', views.SubjectNamesView.as_view(), name='subject_names'),
    path('schedules/<str:username>/<str:schedule_name>/subjects', views.SubjectsView.as_view(), name='subjects'),

    # delete
    path('schedules/<str:username>/<str:schedule_name>/<str:model>/delete', views.DeleteDataView.as_view(), name='delete_data'),
    path('schedules/<str:username>/<str:schedule_name>/delete', views.DeleteScheduleView.as_view(), name='delete_schedule'),

    # upload data
    path('schedules/<str:username>/<str:schedule_name>/<str:model>/upload', views.UploadDataView.as_view(), name='upload_data'),

    # settings
    path('schedules/<str:username>/<str:schedule_name>/settings', views.ScheduleSettingsView.as_view(), name='settings'),


    # path('create_schedule', views.create_schedule, name='create-schedule'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
