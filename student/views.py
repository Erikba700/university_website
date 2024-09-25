from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, TemplateView

from .forms import RegisterForm, UserLoginForm
from .models import StudentProfile


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
        return reverse('student:studentMain', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')

    def form_invalid(self, form):
        return HttpResponse('Invalid login')


class StudentMainPageView(TemplateView):
    model = StudentProfile
    template_name = "users/student_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student_pk = self.kwargs.get('pk')
        student_profile = get_object_or_404(StudentProfile, user__id=student_pk)

        context['student_data'] = student_profile
        return context
