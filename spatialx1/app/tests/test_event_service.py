import unittest
from unittest.mock import MagicMock, patch
from app.services.event_service import EventService

class TestEventService(unittest.TestCase):
    @patch('app.services.event_service.EventProcessorFactory')
    @patch('app.services.event_service.EventRepository')
    @patch('app.services.event_service.NotificationService')
    def test_process_event_success(self, mock_notification_service, mock_event_repository, mock_event_processor_factory):
        # Mock data
        event_data = {"user_id": "test_user", "type": "test_event", "time_stamp": "2024-03-28 12:00:00"}

        # Mock EventProcessor
        mock_event_processor = MagicMock()
        mock_event_processor_factory.create_event_processor.return_value = mock_event_processor

        # Mock EventRepository
        mock_event_repository_instance = mock_event_repository.return_value
        mock_event_repository_instance.add_item.return_value = None

        # Mock NotificationService
        mock_notification_service_instance = mock_notification_service.return_value
        mock_notification_service_instance.notify_user.return_value = None

        # Call the method under test
        EventService.process_event(event_data)

        # Assert that EventProcessor's process method was called with the event data
        mock_event_processor.process.assert_called_once_with(event_data)

        # Assert that EventRepository's add_item method was called with the event data
        mock_event_repository_instance.add_item.assert_called_once_with(event_data)

        # Assert that NotificationService's notify_user method was called with the correct arguments
        mock_notification_service_instance.notify_user.assert_called_once_with("test_user", "Event processed successfully ")

    @patch('app.services.event_service.EventProcessorFactory')
    @patch('app.services.event_service.EventRepository')
    def test_process_event_exception(self, mock_event_repository, mock_event_processor_factory):
        # Mock data
        event_data = {"user_id": "test_user", "type": "test_event", "time_stamp": "2024-03-28 12:00:00"}

        # Mock EventProcessor
        mock_event_processor = MagicMock()
        mock_event_processor.process.side_effect = Exception("Test Exception")
        mock_event_processor_factory.create_event_processor.return_value = mock_event_processor

        # Mock EventRepository
        mock_event_repository_instance = mock_event_repository.return_value
        mock_event_repository_instance.add_item.return_value = None

        # Call the method under test
        result = EventService.process_event(event_data)

        # Assert that EventRepository's add_item method was not called due to exception
        mock_event_repository_instance.add_item.assert_not_called()

        # Assert that the method returns False due to the exception
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
