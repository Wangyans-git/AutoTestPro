#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 2024/5/24 17:34
# @Author  : yansheng.wang
# @File    : api_mqtt.py
# @Description : 作用


import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))
    print("Message topic: ", message.topic)
    print("QoS: ", message.qos)
    print("retain flag: ", message.retain)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username="e3d85d3d-eaa8-4070-b7e3-8ac64b33f9c1",password="e3d85d3d-eaa8-4070-b7e3-8ac64b33f9c1")
client.connect("dev-mqtt.openapi.govee.com", 8883, 60)
client.subscribe("GA/e3d85d3d-eaa8-4070-b7e3-8ac64b33f9c1")

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
client.loop_forever()


try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopping the MQTT client.")