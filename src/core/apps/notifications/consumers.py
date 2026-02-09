import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

from .models import Notification

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = parse_qs(self.scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        self.user = await self.get_user_from_token(token)

        await self.accept()  

        if self.user is None:
            await self.send(text_data=json.dumps({
                "error": "Authentication failed"
            }))
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)


    @database_sync_to_async
    def get_user_from_token(self, token):
        if not token:
            return None
        try:
            validated_token = UntypedToken(token)
            jwt_auth = JWTAuthentication()
            user, _ = jwt_auth.get_user(validated_token), validated_token
            return user
        except (InvalidToken, TokenError):
            return None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Called when a message is sent via group_send
    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
