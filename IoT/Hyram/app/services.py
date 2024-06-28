import json
import paho.mqtt.client as mqtt
from functools import lru_cache
from .models import Information


class Mqtt():

    def __init__(self):
        self.client = mqtt.Client()
        # self.client.username_pw_set("Lijiang", "98756545Tn@")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.loop_started = False
        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        print('Connected!')

    @staticmethod
    def on_message(client, userdata, msg):
        print(f'msg_topic:{msg.topic} message:{str(msg.payload)}')
        payload = json.loads(msg.payload.decode())
        Information.objects.create(
            humidity=float(payload['humidity']),
            temperature=float(payload['temperature']),
            moisture=float(payload['moisture'])
        )

    def get_client(self):
        return self.client

    def publish_message(self, topic, message):
        if not self.connected:
            return

        self.client.publish(topic, message)

        # new_message = Messages(
        #     topic=topic,
        #     device="webappwei",
        #     message=message,
        #     type=Messages.SENT
        # )

        # new_message.save()

    def connect(self):
        if self.connected:
            return
        self.client.connect("broker.emqx.io", 1883, 60)
        self.connected = True

    def subscribe(self, topic):
        if not self.connected:
            return
        # for topic in topics:
        self.client.subscribe(topic)
        print(f'subscribed in {topic}')

    def start_loop(self):
        if self.loop_started:
            return

        if not self.connected:
            return

        self.client.loop_start()
        self.loop_started = True
        print('started_loop!')


@lru_cache(maxsize=None)
def get_mqtt():
    return Mqtt()
