from django.conf.urls import url

from .consumers import testConsumer

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', testConsumer),
]