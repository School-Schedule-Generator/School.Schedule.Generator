from django.shortcuts import HttpResponseRedirect
from ..forms import *
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.shortcuts import redirect

class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'generatorApp/login.html'
    success_url = reverse_lazy('generatorApp:home')
    next_page = reverse_lazy('generatorApp:home')


class RegisterUserView(CreateView):
    form_class = RegisterForm
    template_name = 'generatorApp/register.html'
    success_url = reverse_lazy('generatorApp:home')
    next_page = reverse_lazy('generatorApp:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return redirect(self.success_url)


class LogoutUserView(LoginRequiredMixin, View):
    login_url = reverse_lazy('generatorApp:login')

    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('generatorApp:home'))
