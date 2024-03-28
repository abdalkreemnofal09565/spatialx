import requests
from app.config.config import Config
from app.repositories.notification_repository import NotificationRepository

class NotificationService:
    @staticmethod
    def notify_user(user_id, message):
        try:
            endpoint = Config.NOTIFY_API_ENDPOINT
            data = {'user_id': user_id, 'message': message}
            response = requests.post(endpoint, json=data)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            print(f"Notification sent to user {user_id}: {message}")
        except requests.RequestException as e:
            print(f"Failed to send notification: {e}")
