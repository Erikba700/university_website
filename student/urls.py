from django.urls import path
from student import views
from .views import RegisterView, StudentMainPageView, UserLoginView, UserLogoutView

app_name = 'student'

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path("student-main/<int:pk>/", StudentMainPageView.as_view(), name="studentMain"),
    path("student-main/<int:pk>/events/", views.StudentEventsPageView.as_view(), name="studentEvents"),
    path("student-main/<int:pk>/all-events/", views.StudentAllEventsPageView.as_view(), name="studentAllEvents"),
    path("student-main/<int:student_pk>/events/<int:event_pk>/", views.EventDetailView.as_view(), name="studentEventsDetails"),
    path("student-main/<int:pk>/all-courses/", views.AllCourses.as_view(), name="studentAllCourses"),
    path("student-main/<int:student_pk>/courses/<int:course_pk>/", views.CourseDetailView.as_view(), name="studentCoursesDetails"),

    path('reset_password/', views.MyPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
