from rest_framework import generics
from rest_framework.generics import ListAPIView

from programs.models import Program
from programs.api.serializers import ProgramSerializer

class ProgramListView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

class ProgramDetailView(generics.RetrieveAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
