from django.urls import path
from .views import (
    StudentProfileListCreateView,
    StudentProfileDetailView,
    EventsListCreateView,
    EventsDetailView,
    CoursesListCreateView,
    CoursesDetailView,
)

app_name = 'student-api'

urlpatterns = [
    path('student-profiles/', StudentProfileListCreateView.as_view(), name='student-profile-list-create'),
    path('student-profiles/<int:pk>/', StudentProfileDetailView.as_view(), name='student-profile-detail'),

    path('events/', EventsListCreateView.as_view(), name='events-list-create'),
    path('events/<int:pk>/', EventsDetailView.as_view(), name='events-detail'),

    path('courses/', CoursesListCreateView.as_view(), name='courses-list-create'),
    path('courses/<int:pk>/', CoursesDetailView.as_view(), name='courses-detail'),
]
