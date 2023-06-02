import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.template.loader import get_template
from .models import *
from django.contrib.auth.models import User


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

        userch = data.get("message")
        userr = User.objects.all()
        user = ()
        for i in userr:
            # print(i)
            # print(type(i))
            if str(i) == data.get("sender"):
                user = i
        # print(user)
        # print(type(user))

        userre = data.get("r")
        usretarg = data.get("rtarget")


        if not userch:
            return userch

        if not userre or not usretarg:
            chsu = Chatting(cuser=user, chattts=userch)
            chsu.save()

        else:
            parrent = Chatting.objects.get(id=userre)
            chsu = Chatting(cuser=user, chattts=userch, cusrep=parrent, useridhtml=usretarg)
            chsu.save()
        
        payload = {"message": data.get("message"), "sender": data.get("sender"), "r": data.get("rr"), "rtarget": data.get("rtargett")}
        print(payload)

        async_to_sync(self.channel_layer.group_send)(
            f"{self.GROUP_NAME}", {
                "type": "send_message",
                'value': json.dumps(payload)
            }
        )

    def send_message(self, text_data):
        dataa = json.loads(text_data.get("value"))
        # print(dataa.get("r"))        

        self.send(text_data = json.dumps({"payload": dataa}))

    # def user_joined(self, event):
    #     html = get_template("templates/chat.html").render(
    #         context = {"username": event['text']}
    #     )
    #     print(html)
    #     self.send(text_data=html)
