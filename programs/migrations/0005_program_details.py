# Generated by Django 5.1.1 on 2024-09-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0004_remove_test_minimum_grade_program_tests_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='details',
            field=models.CharField(default=0, max_length=550),
            preserve_default=False,
        ),
    ]
