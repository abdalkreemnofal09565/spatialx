from app.utils.json_file_utiles import JSONFileUtils

class BaseRepository:
    def __init__(self, file_path):
        self.json_file_utils = JSONFileUtils(file_path)

    def add_item(self, item):
        self.json_file_utils.add_item(item)

    def get_items(self):
        return self.json_file_utils.get_items()

    def find_by(self, criterion, value):
        return self.json_file_utils.find_by(criterion, value)

