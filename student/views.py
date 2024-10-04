import json
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView, ListView, UpdateView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from programs.models import Events, Courses
from .forms import RegisterForm, UserLoginForm, StudentProfileSearchForm, UserUpdateForm, StudentProfileUpdateForm
from .models import StudentProfile, ChatMessage, ChatRoom


class MyPasswordResetView(PasswordResetView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
        profile = get_object_or_404(StudentProfile, user_id=user_pk)
        if profile.user != self.request.user:
            return 0
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_profile = self.get_student_profile()
        if student_profile == 0:
            raise Exception("You are not allowed to see this page!")
        context['student_data'] = student_profile
        context['student_courses'] = student_profile.chosen_courses.all()
        context['student_events'] = student_profile.events.all()
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


class AllCourses(StudentProfileMixin, TemplateView):
    template_name = "users/courses/all_courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_courses = Courses.objects.all()
        context['all_courses'] = all_courses

        return context


class CourseDetailView(View):
    def get(self, request, student_pk, course_pk):
        courses_ = get_object_or_404(Courses, pk=course_pk)
        student_profile = get_object_or_404(StudentProfile, user_id=student_pk)
        is_joined = courses_ in student_profile.chosen_courses.all()

        context = {
            'course': courses_,
            'is_joined': is_joined,
            'student_data': student_profile,
        }
        return render(request, 'users/courses/course_details.html', context)

    def post(self, request, student_pk, course_pk):
        courses_ = get_object_or_404(Courses, pk=course_pk)
        student_profile = get_object_or_404(StudentProfile, user_id=student_pk)

        if 'join' in request.POST:
            student_profile.chosen_courses.add(courses_)
        elif 'leave' in request.POST:
            student_profile.chosen_courses.remove(courses_)

        return redirect('student:studentAllCourses', pk=student_pk)


class StudentMainChatPageView(View):
    def get(self, request, student_pk):
        student_profile = get_object_or_404(StudentProfile, user_id=student_pk)
        other_students = StudentProfile.objects.filter(chosen_major=student_profile.chosen_major)
        if len(list(other_students)) > 5:
            context = {
                'other_students': random.sample(list(other_students), 5),
                'student_data': student_profile,
            }
        else:
            context = {
                'other_students': other_students,
                'student_data': student_profile,
            }
        return render(request, 'users/chats/main_chat_page.html', context)


class StudentChatView(TemplateView):
    template_name = "users/chats/chat_room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_pk = self.kwargs.get('student_pk')
        room_name = self.kwargs.get('room_name')

        student_profile = get_object_or_404(StudentProfile, user__pk=student_pk)

        normalized_room_name = self.normalize_room_name(room_name)

        chat_room = ChatRoom.objects.filter(name=normalized_room_name).first()

        if not chat_room:
            chat_room = ChatRoom.objects.create(name=normalized_room_name)

        messages = ChatMessage.objects.filter(room=chat_room).order_by('timestamp')

        context['room_name'] = normalized_room_name
        context['student_pk'] = student_pk
        context['student_data'] = student_profile
        context['messages'] = messages

        return context

    def normalize_room_name(self, room_name):
        participants = room_name.split('_')
        participants.sort()
        return '_'.join(participants)


@csrf_exempt
@login_required
def save_firebase_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')

        profile = StudentProfile.objects.get(user=request.user)
        profile.firebase_token = token
        profile.save()

        return JsonResponse({'status': 'token saved'})


class StudentProfileSearchView(ListView):
    model = StudentProfile
    template_name = 'users/chats/search_results.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = StudentProfile.objects.all()

        query = self.request.GET.get('query', '')

        if query:
            queryset = queryset.filter(
                user__username__icontains=query
            ) | queryset.filter(
                user__first_name__icontains=query
            ) | queryset.filter(
                user__last_name__icontains=query
            ) | queryset.filter(
                chosen_major__name__icontains=query
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student_pk = self.kwargs.get('student_pk')
        student_data = get_object_or_404(StudentProfile, user_id=student_pk)
        context['student_data'] = student_data

        context['form'] = StudentProfileSearchForm(self.request.GET or None)

        return context


class ProfileSettingsView(UpdateView):
    model = StudentProfile
    template_name = 'users/profile_settings.html'
    context_object_name = 'student_profile'
    form_class = StudentProfileUpdateForm

    def get_object(self, queryset=None):
        student_profile = get_object_or_404(StudentProfile, user=self.request.user)
        return student_profile

    def get_success_url(self):
        return reverse_lazy('student:profile_settings', kwargs={'student_pk': self.object.user.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_pk = self.kwargs.get('student_pk')
        student_data = get_object_or_404(StudentProfile, user_id=student_pk)
        context['student_data'] = student_data
        context['user_form'] = UserUpdateForm(instance=self.object.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserUpdateForm(request.POST, instance=self.object.user)
        profile_form = StudentProfileUpdateForm(request.POST, request.FILES, instance=self.object)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return super().form_valid(profile_form)

        return self.form_invalid(profile_form)
