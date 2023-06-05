from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

from notifications.models import Category, Notification

User = get_user_model()


def send_notification(
    title: str,
    receivers: list[User],
    sender: User,
    notification_type: str,
    message: str = None,
    category: Category = None,
    real_time_notification: bool = False,
):
    """
    This function will create in app notification with required details.

    Parameters:
    1. title : string
    2. receivers : List of User model instance
    3. sender : User model instance
    4. notification_type :
        a. success
        b. error
        c. warning
        d. info
    5. message : string
    6. category : Category Model instance
    7. notification_status :
        a. read
        b. unread
        c. deleted
    8. real_time_notification : bool (Set True if you want to implement Real Time Notifications)
    """
    if len(receivers) == 0:
        return "Please provide atleast one receiver."
    if notification_type not in list(
        dict(Notification.NotificationTypes.choices).keys()
    ):
        return "Please provide valid notification type. It should be one of ['success', 'error', 'warning', 'info']."

    notification = Notification.objects.create(
        title=title,
        message=message,
        category=category,
        sender=sender,
        notification_type=notification_type,
        state=Notification.NotificationState.unread,
    )
    for receiver in receivers:
        notification.receivers.add(receiver)

    if real_time_notification:
        channel_layer = get_channel_layer()
        # Trigger message sent to group
        for receiver in receivers:
            async_to_sync(channel_layer.group_send)(
                f"notifications_{receiver.pk}",  # Group Name, Should always be string
                {
                    "type": "notify",  # Custom Function written in the consumers.py
                    "message": {"title": title, "message": message},
                },
            )
    return "Notification sent successfully."


def get_notifications(user, notification_status=None):
    if not notification_status:
        return Notification.objects.prefetch_related("receivers").filter(receivers=user)

    if notification_status not in list(
        dict(Notification.NotificationStatus.choices).keys()
    ):
        return "Please provide valid notification status. It should be any of ['read', 'unread', 'deleted']."
    else:
        return Notification.objects.prefetch_related("receivers").filter(
            receivers=user, notification_status=notification_status
        )


def mark_as_read(user):
    Notification.objects.filter(
        receivers=user, notification_status=Notification.NotificationStatus.unread
    ).update(notification_status=Notification.NotificationStatus.read)


def mark_as_unread(user):
    Notification.objects.filter(
        receivers=user, notification_status=Notification.NotificationStatus.read
    ).update(notification_status=Notification.NotificationStatus.unread)
