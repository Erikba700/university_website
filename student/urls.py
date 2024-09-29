from django.urls import path
from student import views
from .views import RegisterView, StudentMainPageView, UserLoginView, StudentCalendarPageView, UserLogoutView

app_name = 'student'

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path("student-main/<int:pk>/", StudentMainPageView.as_view(), name="studentMain"),
    path("student-main/<int:pk>/calendar/", StudentCalendarPageView.as_view(), name="studentCalendar"),

    path('reset_password/', views.MyPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
