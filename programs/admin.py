from django.contrib import admin

from .models import Program, Test, ProgramTestRequirement, Institutes, Events, Courses

admin.site.register(Program)
admin.site.register(ProgramTestRequirement)
admin.site.register(Test)
admin.site.register(Institutes)
admin.site.register(Events)
admin.site.register(Courses)



