from app.repositories.base_repository import BaseRepository

class NotificationRepository(BaseRepository):
    def __init__(self):
        super().__init__('data/notifications.json')
