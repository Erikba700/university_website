from django.contrib import admin

from .models import StudentProfile, ChatMessage, ChatRoom

admin.site.register(StudentProfile)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)

