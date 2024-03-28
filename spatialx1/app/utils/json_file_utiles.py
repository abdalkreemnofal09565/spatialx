import json
import os

class JSONFileUtils:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_absolute_file_path(self):
        # Get the directory where the current script is located
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the absolute file path relative to the script directory
        absolute_path = os.path.join(script_dir, self.file_path)

        return absolute_path

    def read_data(self):
        file_path = self.get_absolute_file_path()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                return data
            except FileNotFoundError:
                return []
        else:
            return []

    def write_data(self, data):
        file_path = self.get_absolute_file_path()
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def add_item(self, event):
        events = self.read_data()
        events.append(event)
        self.write_data(events)

    def get_items(self):
        return self.read_data()

    def find_by(self, criterion, value):
        events = self.read_data()
        return [event for event in events if event.get(criterion) == value]
