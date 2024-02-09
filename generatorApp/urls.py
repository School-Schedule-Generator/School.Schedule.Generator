from django.urls import path
from . import views

app_name = "generatorApp"
urlpatterns = [
    path('login-register/', views.login_register, name='login_register'),
    path('login-register/login/', views.login_page, name='login'),
    path('login-register/register/', views.register_page, name='register'),
    path('home/', views.home, name='home')
]
