import datetime

def get_duration_minutes(last_event_timestamp, current_timestamp):
    # Parse timestamps from strings to datetime objects
    last_event_time = datetime.datetime.strptime(last_event_timestamp, "%Y-%m-%d %H:%M:%S")
    current_time = datetime.datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S")

    # Calculate idle time
    idle_time = current_time - last_event_time
    idle_seconds = idle_time.total_seconds()
    idle_minutes = idle_seconds / 60
    return idle_minutes
