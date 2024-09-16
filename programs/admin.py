from django.contrib import admin

from .models import Program, Test, ProgramTestRequirement

admin.site.register(Program)
admin.site.register(ProgramTestRequirement)
admin.site.register(Test)


