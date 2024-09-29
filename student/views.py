from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, TemplateView

from .forms import RegisterForm, UserLoginForm
from .models import StudentProfile
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.conf import settings


class MyPasswordResetView(PasswordResetView):
    template_name = "auth/reset_password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_code'] = settings.LANGUAGE_CODE
        return context

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = "auth/password_reset_sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_code'] = settings.LANGUAGE_CODE
        return context


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "auth/password_reset_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_code'] = settings.LANGUAGE_CODE
        return context


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "auth/password_reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_code'] = settings.LANGUAGE_CODE
        return context


class RegisterView(FormView):
    template_name = "users/registration.html"
    form_class = RegisterForm
    success_url = reverse_lazy('static_webpages:main')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'You have successfully signed up!')
        return super().form_valid(form)


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        print(self.request.user.pk)
        return reverse('student:studentMain', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)
        if user is None:
            return HttpResponse('Invalid login')

        if not user.is_active:
            return HttpResponse('Disabled account')

        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login')
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('static_webpages:main'))


class StudentMainPageView(TemplateView):
    model = StudentProfile
    template_name = "users/student_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs.get('pk')
        student_profile = get_object_or_404(StudentProfile, user_id=user_pk)

        context['student_data'] = student_profile

        return context


class StudentCalendarPageView(TemplateView):
    template_name = "users/calendar.html"
