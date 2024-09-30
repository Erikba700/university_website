# Generated by Django 5.1.1 on 2024-09-29 11:26

import django.core.validators
import student.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_studentprofile_chosen_courses_studentprofile_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='admission_year',
            field=models.IntegerField(blank=True, default=student.models.current_year, null=True, validators=[django.core.validators.MinValueValidator(2018), django.core.validators.MaxValueValidator(2024)]),
        ),
    ]
