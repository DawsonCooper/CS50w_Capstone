import json
from channels.generic.websocket import WebsocketConsumer


class MessageConsumer(WebsocketConsumer):
    # handle inital connection to client
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'link_is_connected',
            'message': 'Connected to django channels'
        }))
    # handle additional requests/messages from client

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))
    #

    def disconnect(self, code):
        return super().disconnect(code)
