from django.conf.urls import url

from .consumers import UserConsumer

websocket_urlpatterns = [
    url(r'^ws/api/users/$', UserConsumer),
]