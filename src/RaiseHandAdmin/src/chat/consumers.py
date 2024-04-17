import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ..models import group
from channels.db import database_sync_to_async
from django.core.cache import cache


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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
        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
     )

    async def disconnect_group(self):
       
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.disconnect"}
        )

    async def chat_disconnect(self, event):
      
          await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": "destroy224weewrw3"}
            )
    
    @database_sync_to_async
    def add_message(self, id, message, room_name):
        try:
       
             msg = group.objects.get(id=id)
             msg.retracted = False
             msg.save()
        except group.DoesNotExist:
             instance = group(id=id, name=message, groupcode=room_name)
             instance.save()
    
             
             

    @database_sync_to_async
    def remove_message(self, id):
        msg = group.objects.get(id=id)
        msg.retracted = True
        msg.save()
    async def receive(self, text_data):
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



