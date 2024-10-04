from rest_framework import generics

from .serializers import StudentProfileSerializer, EventsSerializer, CoursesSerializer
from ..models import StudentProfile, Events, Courses


class StudentProfileListCreateView(generics.ListCreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class StudentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class EventsListCreateView(generics.ListCreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


class EventsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


class CoursesListCreateView(generics.ListCreateAPIView):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer


class CoursesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer
