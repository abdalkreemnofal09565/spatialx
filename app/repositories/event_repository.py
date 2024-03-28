from app.repositories.base_repository import BaseRepository

class EventRepository(BaseRepository):
    def __init__(self,file_path):
        super().__init__(file_path)
