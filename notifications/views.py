from notifications.notifications import PushNotificationService
from student.models import StudentProfile


def handle_message_event(sender, recipient, message_text):
    recipient_profile = StudentProfile.objects.get(user=recipient)

    if recipient_profile.firebase_token:
        push_service = PushNotificationService(api_key='BJUhmkSUPM9xAQ8lf1olPDZSdjOwz2yA94OK605LTKMoIcoYSwGh91F2oEtDQ4gJqVPue_v_-YAeX6IPerpxnQc')
        title = f"New message from {sender.first_name}"
        body = message_text
        push_service.send_push_notification(recipient_profile.firebase_token, title, body)

