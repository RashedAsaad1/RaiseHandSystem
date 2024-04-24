import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ..models import group
from channels.db import database_sync_to_async
from django.core.cache import cache


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Asynchronous method to connect a user to a chat room. It sets the username, room name, and room group name 
        for the user. It also checks if a cache key exists for the first user of the group. If it does, it retrieves 
        and prints the cached value. If it doesn't, it sets the cache key with the current user's username.

        Attributes:
            self.username (str): The username of the user.
            self.room_name (str): The name of the chat room.
            self.room_group_name (str): The group name of the chat room, prefixed with 'chat_'.
            group_name (str): The name of the group, retrieved from the scope's url_route kwargs.
            cache_key_first_user (str): The cache key for the first user of the group, prefixed with 'first_user_'.

        Side Effects:
            Sets the username, room name, and room group name for the user.
            Retrieves and prints the cached value if cache key exists.
            Sets the cache key with the current user's username if cache key does not exist.
        """
        self.username = self.scope["user"].username
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        group_name = self.scope['url_route']['kwargs']['room_name']
        cache_key_first_user = f'first_user_{group_name}'

        #har får vi group owner
        if cache.get(cache_key_first_user) is not None:
            cached_value = cache.get(cache_key_first_user)
            print(cached_value)
        else:
            cache.set(cache_key_first_user, self.scope["user"].username)
        # lägger vi ett client till groupen
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        

        await self.accept()

    async def disconnect(self, close_code):
        """
        Asynchronous method to disconnect a user from a chat room. It discards the user's channel from the room group.

        Args:
            close_code (int): The code that signifies why the connection was closed.

        Attributes:
            self.room_group_name (str): The group name of the chat room, prefixed with 'chat_'.
            self.channel_name (str): The name of the user's channel.

        Side Effects:
            Discards the user's channel from the room group.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def disconnect_group(self):
        """
        Asynchronous method to send a disconnect message to all users in a chat room. It sends a 'chat.disconnect' 
        message to the room group.

        Attributes:
            self.room_group_name (str): The group name of the chat room, prefixed with 'chat_'.

        Side Effects:
            Sends a 'chat.disconnect' message to the room group.
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.disconnect"}
        )
    async def chat_disconnect(self, event):
        """
        Asynchronous method to send a disconnect message to all users in a chat room. It sends a 'chat.message' 
        with a specific message to the room group.

        Args:
            event (dict): An event dictionary that contains the 'type' of the event.

        Attributes:
            self.room_group_name (str): The group name of the chat room, prefixed with 'chat_'.

        Side Effects:
            Sends a 'chat.message' with a specific message to the room group.
        """
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": "destroy224weewrw3"}
        )
    @database_sync_to_async
    def add_message(self, id, message, room_name):
        """
        Asynchronous method to add a message to a group. It tries to get a group with the given id. If it exists, 
        it sets the 'retracted' attribute of the group to False and saves the group. If it doesn't exist, it creates 
        a new group with the given id, message as name, and room_name as groupcode, and saves the group.

        This method is decorated with 'database_sync_to_async' to allow synchronous database operations to be 
        performed inside an asynchronous context.

        Args:
            id (int): The id of the group.
            message (str): The message to be set as the name of the group.
            room_name (str): The name of the room to be set as the groupcode of the group.

        Side Effects:
            Modifies the 'retracted' attribute of the group if it exists.
            Creates and saves a new group if it doesn't exist.
        """
        try:
            msg = group.objects.get(id=id)
            msg.retracted = False
            msg.save()
        except group.DoesNotExist:
            instance = group(id=id, name=message, groupcode=room_name)
            instance.save()

  
    @database_sync_to_async
    def remove_message(self, id):
        """
    Asynchronous method to mark a message as retracted in a group. It gets a group with the given id, 
    sets the 'retracted' attribute of the group to True, and saves the group.

    This method is decorated with 'database_sync_to_async' to allow synchronous database operations to be 
    performed inside an asynchronous context.

    Args:
        id (int): The id of the group.

    Side Effects:
        Modifies the 'retracted' attribute of the group.
          """
        msg = group.objects.get(id=id)
        msg.retracted = True
        msg.save()
    async def receive(self, text_data):
        """
    Asynchronous method to receive and process a message. It loads the message from JSON, retrieves the message 
    type, and performs different actions based on the type. If the type is 'destroy', it checks if the sender is 
    the group owner and disconnects the group if true. If the type is 'add', it adds the message to the group and 
    sends it to the room group. If the type is 'remove', it removes the message from the group and sends a removal 
    message to the room group.

    Args:
        text_data (str): The text data received, in JSON format.

    Side Effects:
        Modifies the group and sends messages to the room group based on the message type.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        id = text_data_json["id"]
        type = text_data_json["type"]
        group_name = self.scope['url_route']['kwargs']['room_name']
        cache_key = f'messages_{group_name}'
        group_name = self.scope['url_route']['kwargs']['room_name']
        cache_key_first_user = f'first_user_{group_name}'

        cached_messages = cache.get(cache_key, [])
        if type == "destroy":
            #har kollar jag om det är owner som vill sluta conntion 
            if cache.get(cache_key_first_user) == message:
                await self.disconnect_group()
                print("every thing is ok")
            else:
                print("sorry you are not the group owner")

            #har liggar jag namnet på klient som tryckte på knappen
        if type == "add":
            id = text_data_json["id"]
            cached_messages.append(message)
            cache.set(cache_key, cached_messages)

            await self.add_message(id, message, group_name)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message}
            )

            id = text_data_json["id"]
            group_name = self.scope['url_route']['kwargs']['room_name']
            cache_key = f'messages_{group_name}'
            cached_messages = cache.get(cache_key, [])

            await self.add_message(id, message, self.scope['url_route']['kwargs']['room_name'])
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message}
            )
        #har tabort jag namnet på klient som tryckte på knappen
        if type == "remove":
            value_to_remove = text_data_json["message"]
            group_name = self.scope['url_route']['kwargs']['room_name']
            cache_key = f'messages_{group_name}'
            cached_messages = cache.get(cache_key, [])

            if value_to_remove in cached_messages:
                cached_messages.remove(value_to_remove)
                cache.set(cache_key, cached_messages)

                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "chat.message", "message": value_to_remove + "rm"}
                )
            else:
                print("Value not found in cache:", value_to_remove)

            
    async def chat_message(self, event):
        """
    Asynchronous method to process a chat message event. It retrieves the message from the event, adds it to the 
    group, and sends it to all clients. If the message is None, it prints a message indicating that there is 
    nothing to print.

    Args:
        event (dict): An event dictionary that contains the 'message'.

    Side Effects:
        Modifies the group and sends messages to all clients.
        """
        message = event["message"]

        if message != None:

          group_name = self.scope['url_route']['kwargs']['room_name']
          cache_key = f'messages_{group_name}'
          cached_messages = cache.get(cache_key, [])
          cached_messages.append(message)
        
            #har visar all klinter som finns på cach
          for msg in cached_messages:
              print(msg)
              await self.send(text_data=json.dumps({"message": msg}))

        else:
            print ("nothing to print")



