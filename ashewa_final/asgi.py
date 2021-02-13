import os

from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path 

class CustomSocketioProtocolTypeRouter(ProtocolTypeRouter):
    """
    Overrided base class's __call__ method to support python socketio 4.2.0 and daphne 2.3.0
    """
    def __call__(self, scope, *args):
        if scope["type"] in self.application_mapping:
            handlerobj = self.application_mapping[scope["type"]](scope)
            if args:
                return handlerobj(*args)
            return handlerobj
        raise ValueError(
            "No application configured for scope type %r" % scope["type"]
        )

application = CustomSocketioProtocolTypeRouter({
    # "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    # "websocket": URLRouter([
    #     path('graphql/', GraphqlSubscriptionConsumer)
    # ]),
})