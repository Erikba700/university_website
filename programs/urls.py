from django.urls import path
from .views import ProgramListView, ProgramDetailView, ProgramSearchView, InstitutesListView, InstituteDetailView

app_name = 'programs'

urlpatterns = [
    path('programs/', ProgramListView.as_view(), name='program-list'),
    path('programs/<int:pk>/', ProgramDetailView.as_view(), name='program-detail'),
    path('institutes/', InstitutesListView.as_view(), name='institute-list'),
    path('institutes/<int:pk>/', InstituteDetailView.as_view(), name='institute-detail'),
    path('search/', ProgramSearchView.as_view(), name='program-search'),
]
