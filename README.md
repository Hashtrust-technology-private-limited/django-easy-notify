# django-app-notifications

django-notifications is Django App to create/send notification by calling just hit of single function.

Quick Start
-----------
1. Add 'notifications' to your INSTALLED_APPS setting like this::
    ```
    INSTALLED_APPS = [
        ...
        'notifications',
    ]
    ```
2. Run ``python manage.py migrate`` to create the django-mails models.
3. Add Templates path to your TEMPLATES in setting.py
4. import method to send email ``from notifications.utils import send_notification``
5. Use method ``from notifications.utils import get_notifications`` to receive notifications based on status/all notifications.


Description
-----------
# To Send or Create Notification

```
send_notification(
    title : str,
    receivers : list[User],
    sender : User,
    notification_type : str,
    message : str = None,
    category : Category = None,
    real_time_notification : bool = False
)
```
* This function will create in-app notification with required details.

* Parameters:
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
8. real_time_notification : bool (Set True if you want to implement Real-Time Notifications)

# To fetch notifications

```
get_notifications(user, notification_status = None):
```
* Parameters:
1. user : Instance of User Model (Receiver)
2. notification_status :
    a. read
    b. unread
    c. deleted
    Note : Set None to receive all notifications.

# Mark as Read
```
mark_as_read(user)
```
* Parameters:
1. user : Instance of User Model (Receiver)

# Mark as Unread
```
mark_as_unread(user)
```
* Parameters:
1. user : Instance of User Model (Receiver)


Django Channels Setting
-----------------------

```
ASGI_APPLICATION = "django_notifications.asgi.application"
INSTALLED_APPS.insert(0, "channels")
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}
```

* Script to receive Web socket response

```
<script>
    var loc = window.location
    var wsStart = "ws://"
    if (loc.protocol == "https:"){
        wsStart = "wss://"
    }
    var webSocketEndpoint =  wsStart + loc.host + '/ws/notifications/'  // ws : wss   // Websocket URL, Same on as mentioned in the routing.py


    var socket = new WebSocket(webSocketEndpoint) // Creating a new Web Socket Connection

    // Socket On receive message Functionality
    socket.onmessage = function(e){
        console.log('message', e)
        console.log(JSON.parse(e.data)) // Access the notification data
        //$("body").append("<h3>"+e.data+"</h3>")
        // Can write any functionality based on your requirement
    }

    // Socket Connet Functionality
    socket.onopen = function(e){
        console.log('open', e)
    }

    // Socket Error Functionality
    socket.onerror = function(e){
        console.log('error', e)
    }

    // Socket close Functionality
    socket.onclose = function(e){
        console.log('closed', e)
    }
</script>
```
# Setup guideline

- build: Create the build and runtime images
```
    docker-compose build
```

- up: Start up the project
```
    docker-compose up
```
- To see services and their ports
```
    docker ps
```
- shell: Shell into the running Django container
```
    docker exec -it CONTAINER ID /bin/bash
```
- migrate: Changes you have made to your models
```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
```
