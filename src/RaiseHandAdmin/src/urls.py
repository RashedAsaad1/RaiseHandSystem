from django.urls import path

from .views import (
    index,
    login_view,
    register,
    join,
    createroom,
    room,
)
urlpatterns = [
path('', index, name='index'),
path('login/', login_view, name='login_view'),
path('register/', register),
path('join/', join, name="join"),
path('createroom/', createroom, name="createroom"),
path('chat/<str:room_name>/',room, name="room"),


]