import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.template.loader import get_template


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # print(self.channel_name)
        self.GROUP_NAME = 'user-chat'
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )
        self.accept()

        # async_to_sync(self.channel_layer.group_send)(
        #     f"{self.GROUP_NAME}", {
        #         "type": "send_message",
        #         'value': json.dumps({"status": "online"})
        #     }
        # )

        self.send(text_data=json.dumps({"status": 200}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )
        print("disconnected")

    def receive(self, text_data):
        # print(text_data)
        # self.send(text_data=json.dumps(text_data))
        data = json.loads(text_data)

        print(data)
        payload = {"message": data.get("message"), "sender": data.get("sender")}

        async_to_sync(self.channel_layer.group_send)(
            f"{self.GROUP_NAME}", {
                "type": "send_message",
                'value': json.dumps(payload)
            }
        )

    def send_message(self, text_data):
        data = text_data.get("value")
        print(data)

        self.send(text_data = json.dumps({"payload": data}))

    def user_joined(self, event):
        html = get_template("templates/chat.html").render(
            context = {"username": event['text']}
        )
        print(html)
        self.send(text_data=html)
