from app.repositories.base_repository import BaseRepository

class EventRepository(BaseRepository):
    def __init__(self,file_path):
        super().__init__(file_path)
    def find_last_by_user_id_and_type(self, user_id: str, event_type: str):
        # Implement the logic to find the last event for a specific user and type
        # Read all events from the file
        all_events = self.get_items()

        # Filter events by user_id and event_type
        filtered_events = [event for event in all_events if event["user_id"] == user_id and event["type"] == event_type]

        # Sort filtered events by timestamp in descending order
        sorted_events = sorted(filtered_events, key=lambda x: x["time_stamp"], reverse=True)

        # Return the first event (last event based on timestamp) if any
        return sorted_events[0] if sorted_events else None