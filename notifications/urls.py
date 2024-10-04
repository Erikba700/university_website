from django.urls import path
from .views import handle_message_event

urlpatterns = [
    path('send-notification/', handle_message_event, name='send_notification'),
]
