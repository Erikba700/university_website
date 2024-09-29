import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from programs.models import Program, Events, Courses


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admission_year = models.IntegerField(null=True, blank=True, default=datetime.date.today().year,
                                         validators=[
                                             MinValueValidator(int(datetime.date.today().year) - 6),
                                             MaxValueValidator(int(datetime.date.today().year)),
                                         ]
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

