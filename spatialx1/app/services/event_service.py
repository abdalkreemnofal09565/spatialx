import time
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.notification_service import NotificationService
from app.repositories.event_repository import EventRepository
from app.utils.helpers import get_duration_minutes

class EventService:
    scheduler = BackgroundScheduler()

    @staticmethod
    def process_event(event):
        try:
            event_processor = EventProcessorFactory.create_event_processor(event)
            event_processor.process(event)

            # Store the event in the JSON file
            event_repository = EventRepository('..\data\events.json')
            event_repository.add_item(event)
            return True
        except Exception as e:
            # Handle exceptions gracefully, for example, log the error
            print(f"Error processing event: {e}")


class EventProcessor:
    def process(self, event):
        raise NotImplementedError("process method must be implemented in subclasses.")



class TrainingProgramFinishedEventProcessor(EventProcessor):
    def process(self, event):
        try:
            event_repository = EventRepository('..\data\events.json')
            # Find the last training_program_started event for the user
            last_started_event = event_repository.find_last_by_user_id_and_type(event["user_id"], "training_program_started")

            if last_started_event:
                # Parse timestamps from strings to datetime objects
                started_timestamp = last_started_event["time_stamp"]
                finished_timestamp = event["time_stamp"]

                # Calculate duration in minutes
                duration_minutes = get_duration_minutes(started_timestamp, finished_timestamp)

                if duration_minutes > 30:
                    NotificationService.notify_user(event["user_id"], f"Congratulations! You've completed a {duration_minutes}-minute training program.")
            else:
                print("No matching training_program_started event found for the user.")
        except Exception as e:
            # Handle exceptions gracefully, for example, log the error
            print(f"Error processing training program finished event: {e}")


class AppLaunchEventProcessor(EventProcessor):
    def send_encouragement_notification(self, user_id):
        #  code to send the encouragement notification
        NotificationService.notify_user(user_id, "Start training now!")
        pass

    def process(self, event):
        try:
            # Check if the user starts a training program within 10 minutes
            job_id = f"encouragement_{event['user_id']}"

            EventService.scheduler.add_job(self.send_encouragement_notification, 'interval', minutes=1,args=[event['user_id']], id=job_id)
            return True
        except Exception as e:
            # Handle exceptions gracefully, for example, log the error
            print(f"Error processing app launch event: {e}")


class TrainingProgramStartedEventProcessor(EventProcessor):
    def process(self, event):
        try:
            # Cancel the encouragement notification task if it exists
            user_id = event['user_id']
            job_prefix = f"encouragement_{user_id}"
            print(job_prefix)

            for job in EventService.scheduler.get_jobs():
                if job.id.startswith(job_prefix):
                    print(job.id)
                    EventService.scheduler.remove_job(job.id)

            print(EventService.scheduler.get_jobs())

            # Process the training program started event
            NotificationService.notify_user(user_id, "Training program started")
        except Exception as e:
            # Handle exceptions gracefully, for example, log the error
            print(f"Error processing training program started event: {e}")


class TrainingProgramCancelledEventProcessor(EventProcessor):
    def process(self, event):
        try:
            NotificationService.notify_user(event["user_id"], "Training program cancelled")
        except Exception as e:
            # Handle exceptions gracefully, for example, log the error
            print(f"Error processing training program cancelled event: {e}")


class UnknownEventProcessor(EventProcessor):
    def process(self, event):
        # Handle unknown event type gracefully
        # This method can be customized based on the business logic.
        # For example, you can log the event or notify system administrators.
        pass


class EventProcessorFactory:
    @staticmethod
    def create_event_processor(event):
        event_type = event["type"]
        if event_type == 'training_program_finished':
            return TrainingProgramFinishedEventProcessor()
        elif event_type == 'app_launch':
            return AppLaunchEventProcessor()
        elif event_type == 'training_program_started':
            return TrainingProgramStartedEventProcessor()
        elif event_type == 'training_program_cancelled':
            return TrainingProgramCancelledEventProcessor()
        else:
            return UnknownEventProcessor()


# Initialize the scheduler and start it
EventService.scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: EventService.scheduler.shutdown())
