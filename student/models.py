import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from programs.models import Program, Events, Courses


def current_year():
    return datetime.date.today().year


def validate_admission_year(value):
    if value < current_year() - 6 or value > current_year():
        raise ValidationError(f'Admission year must be between {current_year() - 6} and {current_year()}.')


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admission_year = models.IntegerField(
        null=True,
        blank=True,
        default=current_year,
        validators=[validate_admission_year]
    )
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    chosen_major = models.ForeignKey(Program, on_delete=models.PROTECT, null=True, blank=True)
    chosen_courses = models.ManyToManyField(Courses, null=True, blank=True)
    events = models.ManyToManyField(Events, null=True, blank=True)

    def __str__(self):
        return f"Student: {self.user.first_name} {self.user.last_name} {self.user.username}"


@receiver(post_save, sender=User)
def post_save_student(instance, created, **kwargs):
    if created and not hasattr(instance, 'studentprofile'):
        StudentProfile.objects.create(user=instance)


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}: {self.text}"
