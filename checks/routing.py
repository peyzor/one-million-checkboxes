from django.urls import re_path

from checks import consumers

websocket_urlpatterns = [
    re_path("ws/test/", consumers.MyTestConsumer.as_asgi()),
]
