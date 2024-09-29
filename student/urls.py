from django.urls import path
from student import views
from .views import RegisterView, StudentMainPageView, UserLoginView, UserLogoutView, StudentEventsPageView, \
    EventDetailView, StudentAllEventsPageView

app_name = 'student'

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path("student-main/<int:pk>/", StudentMainPageView.as_view(), name="studentMain"),
    path("student-main/<int:pk>/all_events/", StudentAllEventsPageView.as_view(), name="studentAllEvents"),
    path("student-main/<int:pk>/events/", StudentEventsPageView.as_view(), name="studentEvents"),
    path("student-main/<int:student_pk>/events/event-details/<int:event_pk>/", EventDetailView.as_view(),
         name="studentEventsDetails"),

    path('reset_password/', views.MyPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

