import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from programs.models import Program


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admission_year = models.IntegerField(
        validators=[
            MinValueValidator(int(datetime.date.today().year) - 6),  # Ensure value is greater than or equal
            MaxValueValidator(int(datetime.date.today().year))  # Ensure value is less than or equal to current year
        ]
    )
    image = models.ImageField()
    chosen_major = models.ForeignKey(Program, on_delete=models.PROTECT)

    def __str__(self):
        return f"Student: {self.user.first_name} {self.user.last_name}"


@receiver(post_save, sender=User)
def post_save_student(instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)
