from rest_framework import serializers

from programs import models


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Program
        fields = ['id', 'name', 'tests', 'institute']
