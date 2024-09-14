from django.urls import path

from .views import MainPageView, ContactPageView

app_name = 'static_webpages'

urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
    path("contact/", ContactPageView.as_view(), name="contact")
]
