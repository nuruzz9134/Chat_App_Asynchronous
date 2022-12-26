
from django.urls import path
from chat_app import views

urlpatterns = [
    path('<str:group_name>/',views.index),
]