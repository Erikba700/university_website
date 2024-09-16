from django.urls import path
from .views import ProgramListView, ProgramDetailView

app_name = 'programs'

urlpatterns = [
    path('programs/', ProgramListView.as_view(), name='program-list'),
    path('programs/<int:pk>/', ProgramDetailView.as_view(), name='program-detail'),
]
