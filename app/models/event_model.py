class Event:
    def __init__(self, user_id, device_id, event_type, event_timestamp, **kwargs):
        self.user_id = user_id
        self.device_id = device_id
        self.event_type = event_type
        self.event_timestamp = event_timestamp
        self.__dict__.update(kwargs)
