from django.urls import path

from .views import MainPageView, ContactPageView, CampusLifePageView, EventsDetailView

app_name = 'static_webpages'

urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path("campus-life/", CampusLifePageView.as_view(), name="campus"),
    path("events/<int:pk>/", EventsDetailView.as_view(), name="events")
]
