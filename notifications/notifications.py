from pyfcm import FCMNotification


class PushNotificationService:
    def __init__(self, api_key):
        self.fcm = FCMNotification(api_key=api_key)

    def send_push_notification(self, registration_id, title, message):
        result = self.fcm.notify_single_device(
            registration_id=registration_id,
            message_title=title,
            message_body=message,
        )
        return result
