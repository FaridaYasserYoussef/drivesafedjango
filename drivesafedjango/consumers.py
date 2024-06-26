import json
from channels.generic.websocket import WebsocketConsumer


class TripUpdatesConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data = json.dumps({
            'type': 'connection_established',
            'message': 'you are now connected'
        }))