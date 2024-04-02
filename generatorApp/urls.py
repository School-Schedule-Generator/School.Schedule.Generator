from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "generatorApp"
urlpatterns = [
    path('home/', views.home, name='home'),
    path('accounts/login/', views.LoginUserView.as_view(), name='login'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', views.LogoutUserView.as_view(), name='logout'),
    path('docs/', views.DocsView.as_view(), name='docs'),
    path('schedules/', views.SchedulesListView.as_view(), name='schedules_base'),
    path('schedules/<str:username>', views.SchedulesListView.as_view(), name='schedules'),
    path('schedules/<str:user_name>/<int:schedule_id>', views.SchedulesView.as_view(), name='schedule'),

    path('upload/<int:schedule_id>', views.upload, name='upload'),
    path('upload/<str:file_name>/<int:schedule_id>', views.get_upload_file, name='get-upload-file'),
    path('settings/<int:schedule_id>', views.schedule_settings, name='settings'),
    path('create_schedule', views.create_schedule, name='create-schedule'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
