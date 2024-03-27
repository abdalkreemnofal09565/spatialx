import datetime

def get_idle_time(last_event_timestamp, current_timestamp):
    idle_time = current_timestamp - last_event_timestamp
    return idle_time.total_seconds()
