from django.urls import path

from static_webpages.urls import app_name, urlpatterns
from . import views

urlpatterns = [
    path('programs/', views.ProgramListView.as_view(), name='api-program-list'),
    path('programs/<int:pk>/', views.ProgramDetailView.as_view(), name='api-program-detail'),
]
