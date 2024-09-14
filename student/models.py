import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class StudyFields(models.Model):
    course_name = models.CharField(max_length=100)


class ChosenStudyField(models.Model):
    course_choice = [("math_analyses", "Math Analyses")]
    # course_choice = [(c.course.replace(" ", "_").lower, c.course) for c in list(StudyFields.objects.all())]
    chosen_course = models.CharField(max_length=100, choices=course_choice)

    def __str__(self):
        return self.chosen_course


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admission_year = models.IntegerField(
        validators=[
            MinValueValidator(int(datetime.date.today().year) - 6),  # Ensure value is greater than or equal
            MaxValueValidator(int(datetime.date.today().year))  # Ensure value is less than or equal to current year
        ]
    )
    image = models.ImageField()
    study_field = models.ForeignKey('ChosenStudyField', on_delete=models.PROTECT)

    def __str__(self):
        return f"Student: {self.user.first_name} {self.user.last_name}"


@receiver(post_save, sender=User)
def post_save_student(instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)
