from django.urls import path
from .views import main, register

urlpatterns = [
    path("main/", main, name="main"),
    path("registration/", register, name="registration")
]