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
        # print(data)
        
        v = data.get("v")

        if v:
            payload = {"v":v}
            print(payload)

            async_to_sync(self.channel_layer.group_send)(
                f"{self.GROUP_NAME}", {
                    "type": "del_message",
                    'value': json.dumps(payload)
                }
            )

        else:
            userch = data.get("message")
            reus = data.get("remessage")
            reus = reus.replace(str(data.get("cc")), "")
            # print(reus)
            userr = User.objects.all()
            user = get_user_from_string(data.get("sender"))

            userre = data.get("r")
            usretarg = data.get("rtarget")

            name = ""

            if not userch and not reus:
                return userch

            if not userre or not usretarg:
                chsu = Chatting(cuser=user, chattts=userch)
                chsu.save()

            else:
                parrent = Chatting.objects.get(id=userre)
                # print(parrent, type(parrent))
                chsu = Chatting(cuser=user, chattts=reus, cusrep=parrent, useridhtml=usretarg)
                chsu.save()
                name = Chatting.objects.filter(useridhtml=usretarg).first().cusrep

            name = str(name)
            print(name)
            payload = {"message": data.get("message"), "sender": data.get("sender"), "r": userre, "rtarget": usretarg, "reus":reus, "name":name}
            print(payload)

            async_to_sync(self.channel_layer.group_send)(
                f"{self.GROUP_NAME}", {
                    "type": "send_message",
                    'values': json.dumps(payload)
                }
            )

    def send_message(self, text_data):
        dataa = json.loads(text_data.get("values"))
        # print(dataa.get("r"))  

        lusch = Chatting.objects.last()
        usert = get_user_from_string(lusch)

        ll = Chatting.objects.filter(cuser=usert).last().id
        fir = Chatting.objects.first().id
        # print(fir)
        # print(type(ll))      

        self.send(text_data = json.dumps({"payload": dataa, "ll": ll, "fir":fir}))

    # def user_joined(self, event):
    #     html = get_template("templates/chat.html").render(
    #         context = {"username": event['text']}
    #     )
    #     print(html)
    #     self.send(text_data=html)

    def del_message(self, text_dataa):
        data = json.loads(text_dataa.get("value"))
        v = data.get("v")
        v = int(v.replace("del", ""))

        dl = Chatting.objects.filter(id=v)
        dl.delete()
        self.send(text_data = json.dumps({"v":v}))
