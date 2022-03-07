import datetime
import json
import os
import time
import requests
import copy
import paho.mqtt.client as mqtt
from engin_core.line_notify import LineNotifyAgentMixIn


class Cloud108(LineNotifyAgentMixIn):
    def __init__(self, *args, **kwargs):
        self.host = kwargs.get('host', 'https://or.108cloud.io/api/v1/')
        self.api_host = kwargs.get('api_host', "http://localhost:5000")
        self.serial = kwargs.get('serial', 'AK203121707000092')
        self.mqtt = mqtt.Client()
        self.public_topic = 'Slide/Test2'
        self.mqtt_connect_flag = False
        return

    def init_mqtt(self, host='203.170.190.171'):
        lwt_online_val = 'online'
        lwt_offline_val = 'offline'

        mqtt_client = self.mqtt

        mqtt_client.on_connect = self.on_mqtt_connect
        mqtt_client.on_publish = self.on_mqtt_publish
        mqtt_client.on_disconnect = self.on_mqtt_disconnect
        # mqtt_client.will_set(self.public_topic, payload=lwt_offline_val, retain=True)
        # mqtt_client.username_pw_set("home", "12fca5!x")
        return self.connect_mqtt(host)

    def connect_mqtt(self, host="203.170.190.171"):
        mqtt_client = self.mqtt
        try:
            print("Init MQTT host={}".format(host))
            mqtt_client.connect(host, 1883, 60)
            self.mqtt_connect_flag = True
        except Exception as e:
            self.line_notify("MQTT Error : {}".format(e))
            print(e)
        return

    def public_message(self, public_topic, data):
        if self.mqtt_connect_flag is False:
            self.line_notify("MQTT Reconnect")
            self.connect_mqtt()

        self.mqtt.publish(public_topic, data)
        return

    def on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.mqtt_connect_flag = True
            self.line_notify("MQTT Status : connected OK")
        else:
            print("Bad connection Returned code=", rc)
            self.mqtt_connect_flag = False
            self.line_notify("MQTT Status : Bad connection Returned code={}".format(rc))
        return

    def on_mqtt_disconnect(self, *args):
        self.mqtt_connect_flag = False
        self.line_notify("MQTT Status : On disconnect")
        return

    def on_mqtt_publish(self, client, userdata, mid):
        # print('on_mqtt_publish() on_mqtt_publish')
        return

    def pushLog(self, data):
        body = self.create_push_data(data)
        req = requests.post(self.host, data={
            "1o8": body
        }, files=[])
        return body

    def create_push_data(self, data):
        dt = datetime.datetime.now()
        raw_data = [
            self.serial,
            dt.strftime('%Y-%m-%d %H:%M:%S'),
            dt.strftime('%Y-%m-%d'),
            dt.strftime('%H:%M:%S'),
            dt.strftime('%Y-%m-%d %H:%M:%S'),
            '0',
            *data
        ]
        return ",".join(str(x) for x in raw_data)

    def create_mqtt_push_data(self, data):
        dt = datetime.datetime.now()
        raw_data = [
            dt.strftime('%Y-%m-%d %H:%M:%S'),
            dt.strftime('%Y-%m-%d'),
            dt.strftime('%H:%M:%S'),
            dt.strftime('%Y-%m-%d %H:%M:%S'),
            '5',
            *data
        ]
        return ",".join(str(x) for x in raw_data)

    def create_frame(self):
        return ["0" for x in range(100)]

    def fill_data(self, source, data, offset, length):
        out_data = copy.deepcopy(source)
        return out_data[:offset] + data + out_data[offset + length:]

    def push_or_result(self, vir_id, data):
        try:
            req = requests.post("{}/or_result/{}".format(self.api_host, vir_id), data={
               **data
            })
            print(data, req)

        except Exception as e:
            print(e)
        return

    def push_or_analysis(self, vir_id, data):
        try:
            req = requests.post("{}/or_analysis/{}".format(self.api_host, vir_id), data={
               **data
            })
            print(data, req)
        except Exception as e:
            print(e)
        return
