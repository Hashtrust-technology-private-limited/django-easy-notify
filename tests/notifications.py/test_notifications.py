from django.test import TestCase

from notifications.factories import CategoryFactory, NotificationFactory, UserFactory
from notifications.models import Notification
from notifications.utils import get_notifications, send_notification


# Create your tests here.
class TestNotification(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory(username="SenderUser")
        self.category = CategoryFactory()
        self.receivers = [
            UserFactory(username="ReceiverA"),
            UserFactory(username="ReceiverB"),
        ]
        self.notification = NotificationFactory.create(
            title="First Notification", message="Hello World"
        )
        self.notification.receivers.add(self.receivers[0])
        self.real_time_notification = True
        return super().setUp()

    def test_empty_receivers(self):
        response = send_notification(
            title=self.notification.title,
            receivers=[],
            sender=self.notification.sender,
            notification_type=self.notification.notification_type,
            message=self.notification.message,
            category=self.notification.category,
            real_time_notification=self.real_time_notification,
        )
        assert response == "Please provide atleast one receiver."

    def test_invalid_notification_type(self):
        response = send_notification(
            title=self.notification.title,
            receivers=self.receivers,
            sender=self.notification.sender,
            notification_type="other_type",
            message=self.notification.message,
            category=self.notification.category,
            real_time_notification=self.real_time_notification,
        )
        assert (
            response
            == "Please provide valid notification type. It should be one of ['success', 'error', 'warning', 'info']."
        )

    def test_valid_notification(self):
        response = send_notification(
            title=self.notification.title,
            receivers=self.receivers,
            sender=self.notification.sender,
            notification_type=Notification.NotificationTypes.success,
            message=self.notification.message,
            category=self.notification.category,
            real_time_notification=True,
        )
        assert response == "Notification sent successfully."

    def test_get_notifications(self):
        response = get_notifications(self.receivers[0])
        assert len(response) == 1
        assert self.notification.title == response[0]["title"]
