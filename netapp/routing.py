from django.conf.urls import url

# from .consumers import UserConsumer

# websocket_urlpatterns = [
#     url(r'^ws/api/users/$', UserConsumer),
# ]

from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream

events_urlpatterns = [
    url(r'^events/', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'channels': ['test']}),
    url(r'', AsgiHandler),
]