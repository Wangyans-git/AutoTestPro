#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 2024/5/24 14:46
# @Author  : yansheng.wang
# @File    : lan.py
# @Description : 作用


# coding=UTF-8

import time
import socket
import json

# 组播组IP和端口
## ucast_dev_ip = '192.168.50.117'
ucast_dev_port = 4003
mcast_group_ip = '239.255.255.250'
mcast_group_port = 4001


class ApiTest():

    # 组播扫描
    def sender(self):
        # 建立发送socket，和正常UDP数据包没区别
        socket.setdefaulttimeout(60)
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.local_addr = ('', 4002)
        self.send_sock.bind(self.local_addr)
        # self.all_count = int(input("输入需要测试的次数："))
        cmd_json = {
            "msg": {
                "cmd": "scan",
                "data": {
                    "account_topic": "GA/123456789"
                }
            }
        }
        message = json.dumps(cmd_json)
        self.send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        print("**************扫描设备IP**************\r\n")
        try:
            recv_data = self.send_sock.recvfrom(1024)
            recv_msg = recv_data[0]  # 设备信息
            send_addr = recv_data[1]  # ip地址
            print(recv_msg)
            print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
            ucast_dev_ip = send_addr[0]
            t.send_param(ucast_dev_ip)
        except Exception as e:
            print(e)
        time.sleep(2)

    # 单播控制
    def send_param(self, ip):
        count = 0
        # 查询设备

        # ucast_dev_ip = '192.168.50.117'
        # ucast_dev_port = 4003
        print("扫描到的ip地址：：：", ip)

        cmd_json = {
            "msg": {
                "cmd": "devStatus",
                "data": {
                }
            }
        }
        message = json.dumps(cmd_json)
        self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
        try:
            recv_data_dev = self.send_sock.recvfrom(1024)
            recv_msg = recv_data_dev[0]
            send_addr = recv_data_dev[1]
            print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        except Exception as e:
            print(e)
        time.sleep(2)

        # 关机

        while count < 100:  # 循环次数
            cmd_json = {
                "msg": {
                    "cmd": "turn",
                    "data": {
                        "value": 0
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("turn off\r\n")
            time.sleep(2)

            # 开机
            cmd_json = {
                "msg": {
                    "cmd": "turn",
                    "data": {
                        "value": 1
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("turn on\r\n")
            time.sleep(2)

            # 亮度
            cmd_json = {
                "msg": {
                    "cmd": "brightness",
                    "data": {
                        "value": 50
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("set brightness 50\r\n")
            time.sleep(2)

            # 亮度
            cmd_json = {
                "msg": {
                    "cmd": "brightness",
                    "data": {
                        "value": 100
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("set brightness 100\r\n")
            time.sleep(2)

            # 颜色
            cmd_json = {
                "msg": {
                    "cmd": "colorwc",
                    "data": {
                        "color": {
                            "r": 255,
                            "g": 0,
                            "b": 0
                        }
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("set red\r\n")
            time.sleep(2)

            # 颜色
            cmd_json = {
                "msg": {
                    "cmd": "colorwc",
                    "data": {
                        "color": {
                            "r": 0,
                            "g": 255,
                            "b": 0
                        }
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("set green\r\n")
            time.sleep(2)

            # 颜色
            cmd_json = {
                "msg": {
                    "cmd": "colorwc",
                    "data": {
                        "color": {
                            "r": 0,
                            "g": 255,
                            "b": 0
                        }
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("set blue\r\n")
            time.sleep(2)

            # 色温
            cmd_json = {
                "msg": {
                    "cmd": "colorwc",
                    "data": {
                        "colorTemInKelvin": 7000
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("set cw 7000\r\n")
            time.sleep(2)

            # 色温
            cmd_json = {
                "msg": {
                    "cmd": "colorwc",
                    "data": {
                        "color": {"r": 255, "g": 185, "b": 105},
                        "colorTemInKelvin": 3000
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("set cw 3000\r\n")
            time.sleep(5)

            cmd_json1 = {
                "msg": {
                    "cmd": "devStatus",
                    "data": {
                    }
                }
            }
            message = json.dumps(cmd_json1)
            self.send_sock.sendto(message.encode(), (ip, ucast_dev_port))
            print("get status\r\n")
            try:
                recv_data_status = self.send_sock.recvfrom(1024)
                recv_msg = recv_data_status[0]
                send_addr = recv_data_status[1]
                print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
            except Exception as e:
                print(e)
            time.sleep(2)
            count += 1
            print("**************第{}次测试完成**************".format(count))


if __name__ == "__main__":
    t = ApiTest()
    t.sender()
    # t.send_param()

