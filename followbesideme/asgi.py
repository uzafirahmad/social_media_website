"""
ASGI config for followbesideme project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import core.routing
from core.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'followbesideme.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter([
            # core.routing.websocket_urlpatterns
            path('ws/<id>/',ChatConsumer.as_asgi()),
        ])
    )
})