from django.contrib.auth.models import User
from rest_framework import serializers

from programs.models import Program
from ..models import StudentProfile, Events, Courses


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'name', 'details', 'date', 'program']

    def create(self, validated_data):
        event = Events.objects.create(**validated_data)
        return event

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.details = validated_data.get('details', instance.details)
        instance.date = validated_data.get('date', instance.date)
        instance.program = validated_data.get('program', instance.program)
        instance.save()
        return instance


class CoursesSerializer(serializers.ModelSerializer):
    programs = serializers.PrimaryKeyRelatedField(many=True, queryset=Program.objects.all())
    prerequisites = serializers.PrimaryKeyRelatedField(many=True, queryset='self', required=False)

    class Meta:
        model = Courses
        fields = ['id', 'name', 'details', 'duration', 'programs', 'credit', 'grade',
                  'prerequisites']  # Adjust fields as needed

    def create(self, validated_data):
        course = Courses.objects.create(**validated_data)
        return course

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.details = validated_data.get('details', instance.details)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.credit = validated_data.get('credit', instance.credit)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.save()
        instance.programs.set(validated_data.get('programs', instance.programs.all()))
        instance.prerequisites.set(validated_data.get('prerequisites', instance.prerequisites.all()))
        return instance


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    chosen_major = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all(), required=False)
    chosen_courses = serializers.PrimaryKeyRelatedField(many=True, queryset=Courses.objects.all(), required=False)
    events = serializers.PrimaryKeyRelatedField(many=True, queryset=Events.objects.all(), required=False)

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'firebase_token', 'admission_year', 'image', 'chosen_major', 'chosen_courses', 'events']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = User.objects.create(**user_data)
            validated_data['user'] = user
        student_profile = StudentProfile.objects.create(**validated_data)
        return student_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            instance.user.username = user_data.get('username', instance.user.username)
            instance.user.email = user_data.get('email', instance.user.email)
            instance.user.first_name = user_data.get('first_name', instance.user.first_name)
            instance.user.last_name = user_data.get('last_name', instance.user.last_name)
            instance.user.save()

        instance.firebase_token = validated_data.get('firebase_token', instance.firebase_token)
        instance.admission_year = validated_data.get('admission_year', instance.admission_year)
        instance.image = validated_data.get('image', instance.image)
        instance.chosen_major = validated_data.get('chosen_major', instance.chosen_major)

        if 'chosen_courses' in validated_data:
            instance.chosen_courses.set(validated_data['chosen_courses'])

        if 'events' in validated_data:
            instance.events.set(validated_data['events'])

        instance.save()
        return instance
