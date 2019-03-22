# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import netapp.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 'websocket': AuthMiddlewareStack(
    #     URLRouter(
    #         netapp.routing.websocket_urlpatterns
    #     )
    # ),
    'http': URLRouter(netapp.routing.events_urlpatterns),
})
