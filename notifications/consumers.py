import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    # Function to connect to the websocket
    async def connect(self):
        # Checking if the User is logged in
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        if not self.user_id:
            # Reject the connection
            await self.close()
        else:
            self.room_group_name = f"notifications_{self.user_id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    # Function to disconnet the Socket
    async def disconnect(self, close_code):
        await self.close()
        # pass

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    async def notify(self, event):
        await self.send(text_data=json.dumps(event["message"]))
