from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=550)
    tests = models.ManyToManyField(Test, through='ProgramTestRequirement', related_name='programs')

    def __str__(self):
        return self.name


class ProgramTestRequirement(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='test_requirements')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='program_requirements')
    minimum_grade = models.PositiveIntegerField()

    class Meta:
        unique_together = ('program', 'test')

    def __str__(self):
        return f'{self.program.name} - {self.test.name} - Min Grade: {self.minimum_grade}'
