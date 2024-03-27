import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from app.models.event_model import Event
from app.services.notification_service import NotificationService
from app.services.event_service import EventService, EventProcessorFactory

class TestEventService(unittest.TestCase):
    def test_process_event(self):
        # Mock event data
        event_data = {
            "user_id": "foo",
            "device_id": "bar",
            "type": "training_program_finished",
            "training_program_duration": 35,  # More than 30 minutes
            "event_timestamp": datetime.now()
        }
        event = Event(**event_data)

        # Mock the event processor
        event_processor_mock = MagicMock()
        EventProcessorFactory.create_event_processor = MagicMock(return_value=event_processor_mock)

        # Call the process_event method
        EventService.process_event(event)

        # Verify that the event processor's process method is called with the event
        event_processor_mock.process.assert_called_once_with(event)

class TestEventProcessors(unittest.TestCase):
    def test_training_program_finished_event_processor(self):
        # Mock event data
        event_data = {
            "user_id": "foo",
            "device_id": "bar",
            "type": "training_program_finished",
            "training_program_duration": 35,  # More than 30 minutes
            "event_timestamp": datetime.now()
        }
        event = Event(**event_data)

        # Mock NotificationService
        notification_service_mock = MagicMock()
        NotificationService.notify_user = notification_service_mock

        # Call the process method of the TrainingProgramFinishedEventProcessor
        event_processor = TrainingProgramFinishedEventProcessor()
        event_processor.process(event)

        # Verify that NotificationService.notify_user is called with the correct message
        notification_service_mock.assert_called_once_with(event.user_id, "Congratulations! You've completed a 35-minute training program.")

    def test_app_launch_event_processor(self):
        # Mock event data
        event_data = {
            "user_id": "foo",
            "device_id": "bar",
            "type": "app_launch",
            "event_timestamp": datetime.now() - timedelta(minutes=5)  # App launched 5 minutes ago
        }
        event = Event(**event_data)

        # Mock NotificationService
        notification_service_mock = MagicMock()
        NotificationService.notify_user = notification_service_mock

        # Call the process method of the AppLaunchEventProcessor
        event_processor = AppLaunchEventProcessor()
        event_processor.process(event)

        # Verify that NotificationService.notify_user is not called since the user hasn't started a training program within 10 minutes
        notification_service_mock.assert_not_called()

if __name__ == "__main__":
    unittest.main()
