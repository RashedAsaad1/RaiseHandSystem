from django.urls import re_path
from . import consumers

# A list of websocket URL patterns for the application.
websocket_urlpatterns = [
    # The URL route for the chat room, which uses the ChatConsumer.
    re_path(r"wss/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]