from django.urls import path
from chat_app import consumer




websocket_urlpatterns = [
    path('ws/chat/<str:group_name>/',consumer.MyConsumer.as_asgi()),

]
