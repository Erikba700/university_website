from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, TemplateView

from programs.models import Events
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


class StudentProfileMixin:
    def get_student_profile(self):
        user_pk = self.kwargs.get('pk')
        return get_object_or_404(StudentProfile, user_id=user_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_data'] = self.get_student_profile()
        return context


class StudentNavBar(StudentProfileMixin, TemplateView):
    template_name = "users/nav_bar.html"


class StudentMainPageView(StudentProfileMixin, TemplateView):
    template_name = "users/student_main.html"


class StudentEventsPageView(StudentProfileMixin, TemplateView):
    template_name = "users/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_profile = context['student_data']
        context['student_events'] = student_profile.events.all()
        return context


class EventDetailView(View):
    def get(self, request, student_pk, event_pk):
        event = get_object_or_404(Events, pk=event_pk)
        student_profile = get_object_or_404(StudentProfile, user_id=student_pk)
        is_joined = event in student_profile.events.all()

        context = {
            'event': event,
            'is_joined': is_joined,
        }
        return render(request, 'users/events_details.html', context)

    def post(self, request, student_pk, event_pk):
        event = get_object_or_404(Events, pk=event_pk)
        student_profile = get_object_or_404(StudentProfile, user_id=student_pk)

        if 'join' in request.POST:
            student_profile.events.add(event)
        elif 'leave' in request.POST:
            student_profile.events.remove(event)

        return redirect('student:studentEvents', pk=student_pk)


class StudentAllEventsPageView(StudentProfileMixin, TemplateView):
    template_name = "users/all_events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_events = Events.objects.all()
        context['all_events'] = all_events

        return context
