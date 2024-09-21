from django.urls import path
from .views import RegisterView, StudentMainPageView

app_name = 'student'

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("student-main/", StudentMainPageView.as_view(), name="studentMain")
]
