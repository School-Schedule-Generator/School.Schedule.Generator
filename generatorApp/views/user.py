from django.shortcuts import HttpResponseRedirect, render
from ..forms import *
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
import re


class LoginUserView(View):
    form_class = LoginForm
    template_name = 'generatorApp/login.html'
    success_url = reverse_lazy('generatorApp:home')
    next_page = reverse_lazy('generatorApp:home')

    def get(self, request):
        context = {}
        context['error_msg'] = self.request.session.pop('error_msg', '')
        return render(self.request, self.template_name)

    def post(self, request):
        context = {}
        username = self.request.POST.get('login')
        password = self.request.POST.get('password')
        remember_me = self.request.POST.get('remember-me')
        ogg = User.objects.filter(
            Q(email=username) | Q(username=username)
        ).first()

        if not ogg:
            self.request.session['error_msg'] = "Login/e-mail doesn't exist"
            context['error_msg'] = self.request.session['error_msg']
            return render(self.request, self.template_name, context)

        user = authenticate(self.request, username=ogg.username, password=password)

        if user is None:
            self.request.session['error_msg'] = "Invalid password"
            context['error_msg'] = self.request.session['error_msg']
            return render(self.request, self.template_name, context)

        login(self.request, user)

        self.request.session['error_msg'] = None

        if remember_me:
            self.request.session.set_expiry(None)
        else:
            self.request.session.set_expiry(43200)

        return redirect(self.success_url)


class RegisterUserView(View):
    form_class = RegisterForm
    template_name = 'generatorApp/register.html'
    success_url = reverse_lazy('generatorApp:home')

    def get(self, request):
        return render(self.request, self.template_name)

    def post(self, request):
        context = {}
        username = self.request.POST.get('login')
        password1 = self.request.POST.get('password')
        password2 = self.request.POST.get('rpassword')
        email = self.request.POST.get('email')

        if username in User.objects.values_list('username', flat=True):
            self.request.session['error_msg'] = "This username is already taken."
            return render(self.request, self.template_name, context)

        if email in User.objects.values_list('email', flat=True):
            self.request.session['error_msg'] = "This email is already taken."
            return render(self.request, self.template_name, context)

        if password1 != password2:
            self.request.session['error_msg'] = "Please pass in the same password!"
            return render(self.request, self.template_name, context)

        # Individual regex checks for tailored feedback
        if len(password1) < 8:
            self.request.session['error_msg'] = "Password must be at least 8 characters long."
            return render(self.request, self.template_name, context)

        if not re.search(r'[A-Z]', password1):
            self.request.session['error_msg'] = "Password must contain at least one uppercase letter."
            return render(self.request, self.template_name, context)

        if not re.search(r'[a-z]', password1):
            self.request.session['error_msg'] = "Password must contain at least one lowercase letter."
            return render(self.request, self.template_name, context)

        if not re.search(r'[@$!%*?&]', password1):
            self.request.session['error_msg'] = "Password must contain at least one special character (@, $, !, %, *, ?, &)."
            return render(self.request, self.template_name, context)

        user = User.objects.create_user(username, email, password1)
        user.save()
        auth_user = authenticate(username=username, password=password1)
        login(self.request, auth_user)

        self.request.session['error_msg'] = None

        return redirect(self.success_url)


class LogoutUserView(LoginRequiredMixin, View):
    login_url = reverse_lazy('generatorApp:login')

    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('generatorApp:home'))
