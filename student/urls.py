from django.urls import path
from .views import RegisterView, StudentMainPageView, UserLoginView, StudentCalendarPageView, UserLogoutView

app_name = 'student'

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path("student-main/<int:pk>/", StudentMainPageView.as_view(), name="studentMain"),
    path("student-main/<int:pk>/calendar/", StudentCalendarPageView.as_view(), name="studentCalendar"),
]
