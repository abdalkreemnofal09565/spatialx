from app.models.event_model import Event
from app.services.notification_service import NotificationService
import datetime

class EventService:
    @staticmethod
    def process_event(event):
        try:
            event_processor = EventProcessorFactory.create_event_processor(event)
            event_processor.process(event)
        except Exception as e:
            # Handle exceptions gracefully, for example, log the error
            print(f"Error processing event: {e}")

class EventProcessor:
    def process(self, event):
        raise NotImplementedError("process method must be implemented in subclasses.")

class TrainingProgramFinishedEventProcessor(EventProcessor):
    def process(self, event):
        try:
            duration = event.training_program_duration
            if duration > 30:
                minutes_trained = duration
                NotificationService.notify_user(event.user_id, f"Congratulations! You've completed a {minutes_trained}-minute training program.")
        except Exception as e:
            # Handle exceptions gracefully, for example, log the error
            print(f"Error processing training program finished event: {e}")

class AppLaunchEventProcessor(EventProcessor):
    def process(self, event):
        try:
            # Check if the user starts a training program within 10 minutes
            ten_minutes_later = event.event_timestamp + datetime.timedelta(minutes=10)
            if ten_minutes_later <= datetime.datetime.now():
                NotificationService.notify_user(event.user_id, "Start training now!")
        except Exception as e:
            # Handle exceptions gracefully, for example, log the error
            print(f"Error processing app launch event: {e}")

class TrainingProgramStartedEventProcessor(EventProcessor):
    def process(self, event):
        try:
            NotificationService.notify_user(event.user_id, "Training program started")
        except Exception as e:
            # Handle exceptions gracefully, for example, log the error
            print(f"Error processing training program started event: {e}")

class TrainingProgramCancelledEventProcessor(EventProcessor):
    def process(self, event):
        try:
            NotificationService.notify_user(event.user_id, "Training program cancelled")
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
        event_type = event.event_type
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
