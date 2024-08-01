#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
@Time    : 2022/10/11 16:50
@Author  : jhcheng
@FileName: pub_mqtt_717c.py
@SoftWare: PyCharm
"""
# !/usr/bin/env python
# coding:utf-8

import time
import json
import random
from paho.mqtt import client as mqtt_client

# broker = 'broker.emqx.io'  # mqtt代理服务器地址
# port = 1883
broker = 'a3d1vz6v56pkuw-ats.iot.us-east-1.amazonaws.com'  # 代理服务器
# broker = 'aqm3wd1qlc3dy.iot.us-east-1.amazonaws.com'
port = 8883
keepalive = 60  # 与代理通信之间允许的最长时间段（以秒为单位）
# device_topic消息主题
# 测服
GA_topic = "GA/776a304a82aab1763c421ea955bf8b98"  # 消息主题
GD_topics = [
    "GD/542614207b5ecff09d3c2aa47c55289a",
]
client_id = f'python-mqtt-pub-{random.randint(0, 1000)}'  # 客户端id不能重复


class PUB():
    def connect_mqtt(self):
        '''连接mqtt代理服务器'''

        def on_connect(client, userdata, flags, rc):
            '''连接回调函数'''
            # 响应状态码为0表示连接成功
            if rc == 0:
                print("Connected to MQTT OK!")
            else:
                print("Failed to connect, return code %d\n", rc)

        # 连接mqtt代理服务器，并获取连接引用
        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        # 测服
        client.tls_set(ca_certs="D:/pythonProject/python_mqtt/iot_test_cert/rootCA.pem",
                       certfile="D:/pythonProject/python_mqtt/iot_test_cert/b2f000de59-certificate.pem.crt",
                       keyfile="D:/pythonProject/python_mqtt/iot_test_cert/b2f000de59-private.pem.key")

        # # 正服
        # client.tls_set(ca_certs="D:/pythonProject/python_mqtt/iot_qa_cert/root-CA.crt",
        #                certfile="D:/pythonProject/python_mqtt/iot_qa_cert/testIot.cert.pem",
        #                keyfile="D:/pythonProject/python_mqtt/iot_qa_cert/testIot.private.key")
        client.tls_insecure_set(True)
        client.connect(broker, port, keepalive)
        return client

    # 发一次
    def publish_one_time(self, client, data, topic):
        '''发布消息'''
        param = json.dumps(data)
        # 发送数据
        self.pub_one(client, param, topic)

    # 一直循环发送
    def publish_all_the_time(self, client):
        '''发布消息'''
        while True:
            time.sleep(2)
            data = {
                "msg": {
                    "accountTopic": GA_topic,
                    "cmd": "status",
                    "cmdVersion": 0,
                    "transaction": time.time(),
                    "type": 0
                }
            }
            param = json.dumps(data)
            # 发送数据
            self.pub_handle(client, param, GD_topics)

    # 一次发送多个topic
    def pub_handle(self, client, data, topic):
        try:
            for i in range(len(topic)):
                result = client.publish(topic[i], payload=data)  # 发送消息
                status = result[0]
                if status == 0:
                    print(f"Send `{data}` to topic `{topic[i]}`")
                else:
                    print(f"Failed to send message to topic {topic[i]}")
        except Exception as e:
            print(e)

    # 发送一个topic
    def pub_one(self, client, data, topic):
        result = client.publish(topic, payload=data)  # 发送消息
        status = result[0]
        if status == 0:
            print(f"Send `{data}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def get_client(self):
        '''运行发布者'''
        client = self.connect_mqtt()
        return client

    def run(self):
        # '''运行发布者'''
        client = self.get_client()
        self.publish_all_the_time(client)
        # 运行一个线程来自动调用loop()处理网络事件, 非阻塞
        client.loop_start()


if __name__ == '__main__':
    pub = PUB()
    pub.run()
