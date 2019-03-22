# from django.apps import apps
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import AsyncWebsocketConsumer # WebsocketConsumer
# import json
# from rest_framework.renderers import JSONRenderer

# from .serializers import UserSerializer

# class UserConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # self.socket_name = self.scope['url_route']['kwargs']['socket_name']
#         self.socket_name = 'users'
#         self.group_name = 'group_%s' % self.socket_name
#         # Join group
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave group
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         ACCEPTED_ACTIONS = ['CREATE', 'UPDATE', 'DELETE']
#         text_data_json = json.loads(text_data)
#         app_label = text_data_json['app_label']
#         model_name = text_data_json['model_name']
#         instance = text_data_json['instance']
#         username = text_data_json['username']
#         action_msg = text_data_json['action_msg']

#         if action_msg in ACCEPTED_ACTIONS:
#             if action_msg in ['CREATE', 'UPDATE']:
#                 User = apps.get_model(app_label=app_label, model_name=model_name)
#                 instance = User.objects.get(pk=instance, username=username)
#                 serializer = UserSerializer(instance)
#                 message = JSONRenderer().render(serializer.data)
#             else:
#                 message = JSONRenderer().render({
#                     'id': instance,
#                     'username': username,
#                     'msg':'Usuario eliminado'
#                     })
#         else:
#             message = JSONRenderer().render({'msg':'ACCION NO PERMITIDA'})


#         # Send message to group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'user_message',
#                 'message': message,
#                 'action': action_msg
#             }
#         )

#     # Receive message from group
#     async def user_message(self, event):
#         message = event['message']
#         action = event['action']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message.decode("utf-8"),
#             'action': action
#         }))