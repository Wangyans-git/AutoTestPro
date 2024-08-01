#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
@Time    : 2022/10/11 16:50
@Author  : jhcheng
@FileName: sub_mqtt_717c.py
@SoftWare: PyCharm
"""
# !/usr/bin/env python
# coding:utf-8

import random
import base64
from paho.mqtt import client as mqtt_client
import ast
import threading
import time
from common.loger import Loger
from myConfig import setting
from util.handleExcel import HandleExcel
from test_cases.H7171.pub_mqtt3 import PUB

broker = 'a3d1vz6v56pkuw-ats.iot.us-east-1.amazonaws.com'  # 测服代理服务器
# broker = 'aqm3wd1qlc3dy.iot.us-east-1.amazonaws.com'      #正服代理服务器
port = 8883
keepalive = 60  # 与代理通信之间允许的最长时间段（以秒为单位）
# 测服
GA_topic = "GA/776a304a82aab1763c421ea955bf8b98"  # 消息主题    jiahong.cheng@ihoment.com
devices_mac = [
    '32:DD:D0:C9:07:0A:55:6A',
]

GD_topics = [
    "GD/542614207b5ecff09d3c2aa47c55289a",
]

devices_name = ['H717A样签', ]
sku_name = 'H717A'
client_id = f'python-mqtt-sub-{random.randint(0, 1000)}'  # 客户端id不能重复
logers = []
keet_list = {}

# total = 15  # 烧水次数

# 开机
data = {
    "msg": {
        "type": 1,
        "transaction": time.time(),
        "accountTopic": GA_topic,
        "cmd": "turn",
        "data": {
            "val": 1
        }
    }
}


class SUB():
    def __init__(self):
        self.report = setting.TEST_REPORT  # 测试结果
        # # 获取当前时间
        # self.time_start = time.strftime("%Y-%m-%d %H-%M-%S")
        for i in range(len(devices_mac)):
            keet_list["%s" % (i + 1)] = 2
        # 初始化煮水温度表格
        self.handleexcel = HandleExcel(self.report, sku_name)
        self.client_pub = PUB().get_client()
        self.count = 0
        self.row_init = 2
        self.is_add = False
        # self.iot_cert_path = tools.get_iot_cert_path()

    # 创建日志
    def creat_loger(self, device_name):
        for i in range(len(device_name)):
            logers.append(Loger(device_name[i]).get_py_logger())

    # mqtt连接
    def connect_mqtt(self):
        '''连接mqtt代理服务器'''

        def on_connect(client, userdata, flags, rc):
            '''连接回调函数'''
            # 响应状态码为0表示连接成功
            if rc == 0:
                print("Connected to MQTT OK!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        # 测服
        client.tls_set(ca_certs="D:/pythonProject/python_mqtt/iot_test_cert/rootCA.pem",
                       certfile="D:/pythonProject/python_mqtt/iot_test_cert/b2f000de59-certificate.pem.crt",
                       keyfile="D:/pythonProject/python_mqtt/iot_test_cert/b2f000de59-private.pem.key")

        # #正服
        # client.tls_set(ca_certs="D:/pythonProject/python_mqtt/iot_qa_cert/root-CA.crt",
        #                certfile="D:/pythonProject/python_mqtt/iot_qa_cert/testIot.cert.pem",
        #                keyfile="D:/pythonProject/python_mqtt/iot_qa_cert/testIot.private.key")
        client.tls_insecure_set(True)
        client.connect(broker, port, keepalive)
        return client

    # mqtt订阅
    def subscribe(self, client: mqtt_client):
        '''订阅主题并接收消息'''

        def on_message(client, userdata, msg):
            # now = time.strftime("%Y-%m-%d %H-%M-%S")
            # self.wrt_data[0] = now
            '''订阅消息回调函数'''
            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            # 解析数据，得到字符串
            raw_data = msg.payload.decode()
            # 开始数据解析
            self.prase_data_handle(raw_data)

        # 订阅指定消息主题
        client.subscribe(GA_topic)
        client.on_message = on_message

    # 解析数据
    def prase_data_handle(self, raw_data):
        # 将原始数据转化成字典
        status = ast.literal_eval(raw_data)
        if status['cmd'] == 'status':
            # 获取设备mac地址
            d = status['device']

            # 解析和写入温度数据
            for i in range(len(devices_mac)):
                if d == devices_mac[i]:
                    print('我是第%s个：' % (i + 1) + str(d))
                    # 写入日志
                    # logers[i].info(status)
                    print(status)
                    # 拿到command数据
                    command = status['op']['command']
                    # 解析command里面的数据
                    temper = self.prase_data_op(command)
                    if i == 0:
                        # 写入时间
                        time_now = time.strftime("%Y-%m-%d %H-%M-%S")
                        self.handleexcel.write_data(keet_list['%s' % (i + 1)], ((i + 1) * 2) - 1, time_now)
                    # 将数据写入表格
                    self.handleexcel.write_data(keet_list['%s' % (i + 1)], ((i + 1) * 2), int(temper))
                    keet_list['%s' % (i + 1)] += 1

                    # 判断温度是否小于175F，如果小于就自动开机
                    if int(temper) <= 176:
                        if int(status['state']['onOff']) == 0:
                            # 发送开机指令
                            PUB().publish_one_time(self.client_pub, data, GD_topics[i])
                            if self.is_add == False:
                                # 次数没加过，煮水次数加一
                                self.count += 1
                                self.is_add = True
                                # 获取当前时间
                                now = time.strftime("%Y-%m-%d %H-%M-%S")
                                logers[i].info('温度小于80℃，第%s开机煮水，' % self.count + '开机时间%s' % now)
                                # 记录一次数据
                                row_last = self.handleexcel.write_count_data(self.row_init, 1, now, self.count)
                                self.row_init = row_last + 1
                        else:
                            self.is_add = False

    # 解析command
    def prase_data_op(self, command):
        print('command:' + str(command))
        for i in command:
            # 解码
            base64_data = base64.b64decode(i)
            # 转化成16进制字符串
            data = base64_data.hex()
            # format_data = self.format_hex_string(base64_data)
            # 解析当前温度
            if int(data[2], 16) == 1 and int(data[3], 16) == 0:
                # 十六进制转十进制
                raw_num = int(data[6] + data[7] + data[8] + data[9], 16)
                temper = raw_num / 100
                temper = format(temper, '.0f')
                return temper

    # 消息接收
    def run_sub(self):
        # 创建日志
        self.creat_loger(devices_name)
        # 创建表格
        self.handleexcel.creat_excel(devices_name)
        # 创建统计表格
        self.handleexcel.creat_total_excel(devices_name)
        # 运行订阅者
        client = self.connect_mqtt()
        self.subscribe(client)
        #  运行一个线程来自动调用loop()处理网络事件, 阻塞模式
        client.loop_forever()

    # 消息发布
    def run_pub(self):
        PUB().publish_all_the_time(self.client_pub)

    # 测试方法
    def prase_test(self, raw_data):
        status = ast.literal_eval(raw_data)
        # 拿到command数据
        command = status['op']['command']
        # 解析command里面的数据
        temper = self.prase_data_op(command)
        print('temper:' + str(temper))

    def run_thread(self):
        threading.Thread(target=self.run_sub, ).start()
        threading.Thread(target=self.run_pub, ).start()


if __name__ == '__main__':
    sub = SUB()
    sub.run_thread()
