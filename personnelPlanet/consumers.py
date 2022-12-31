import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class MessageConsumer(WebsocketConsumer):
    # handle inital connection to client
    def connect(self):
        self.user = self.scope['user']
        print(self.user.company, self.user.first_name, self.user.id)
        # connects the client to a group using their company name
        self.room_group_name = self.user.company
        print(self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    # handle additional requests/messages from client

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        userId = text_data_json['userId']
        firstName = text_data_json['name']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message,
                'userId': userId,
                'name': firstName
            }
        )
    #

    def send_message(self, event):
        message = event['message']
        userId = event['userId']
        firstName = event['name']
        self.send(text_data=json.dumps({
            'type': 'message',
            'message': message,
            'userId': userId,
            'name': firstName
        }))

    def disconnect(self, code):
        return super().disconnect(code)
