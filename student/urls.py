from django.urls import path
from .views import RegisterView

app_name = 'student'

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration")
]
