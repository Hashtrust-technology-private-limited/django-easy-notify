from django.test import TestCase

from notifications.models import Notification
from notifications.utils import (
    get_notifications,
    mark_as_read,
    mark_as_unread,
    send_notification,
)
from tests.factories import CategoryFactory, NotificationFactory, UserFactory


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
            == f"Please provide valid notification type. It should be any of {list(dict(Notification.NotificationType.choices).keys())}."
        )

    def test_valid_notification(self):
        response = send_notification(
            title=self.notification.title,
            receivers=self.receivers,
            sender=self.notification.sender,
            notification_type=Notification.NotificationType.success,
            message=self.notification.message,
            category=self.notification.category,
            real_time_notification=True,
        )
        assert response == "Notification sent successfully."

    def test_get_notifications(self):
        response = get_notifications(self.receivers[0])
        assert len(response) == 1
        assert self.notification.title == response[0]["title"]

    def test_get_notifications_by_type(self):
        self.warning_notification = NotificationFactory(
            notification_type=Notification.NotificationType.warning
        )
        self.warning_notification.receivers.add(self.receivers[0])
        response = get_notifications(
            self.receivers[0], Notification.NotificationType.warning
        )
        assert len(response) == 1
        assert self.warning_notification.title == response[0]["title"]

    def test_mark_notifications_as_read(self):
        response = mark_as_read(self.receivers[0])
        assert response == f"Notifications of user {self.receivers[0]} marked as read."

    def test_mark_notifications_as_unread(self):
        response = mark_as_unread(self.receivers[0])
        assert (
            response == f"Notifications of user {self.receivers[0]} marked as unread."
        )
