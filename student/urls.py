from django.urls import path
from .views import RegisterView, StudentMainPageView, UserLoginView, StudentCalendarPageView

app_name = 'student'

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("student-main/<int:pk>/", StudentMainPageView.as_view(), name="studentMain"),
    path("student-main/<int:pk>/calendar/", StudentCalendarPageView.as_view(), name="studentCalendar"),
]
