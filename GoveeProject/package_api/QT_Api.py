#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :yansheng.wang
# @File    :
# @Description : 灯带局域网pai
import os

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
import time
import socket
import json
import threading
import sys


class App(object):

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('main.ui')
        self.ui.setMinimumSize(570, 500)
        self.ui.setMaximumSize(570, 500)
        self.ui.scanButton.clicked.connect(self.thread_sender)  # 扫描
        self.ui.goButton.clicked.connect(self.thread_all_run)  # 开始
        self.ui.devButton.clicked.connect(self.thread_devStatus)  # 设备信息
        self.ui.clearButton.clicked.connect(self.clear_display)  # 清除
        self.ui.countButton.clicked.connect(self.test_count)  # 次数
        self.ui.quitButton.clicked.connect(self.quit_app)  # 推出
        # api ip和端口
        self.ucast_dev_port = 4003
        self.mcast_group_ip = '239.255.255.250'
        self.mcast_group_port = 4001

        self.count = 0  # 测试次数

    """
        运行线程
    """

    # 扫描设备ip
    def thread_sender(self):
        thread = threading.Thread(target=self.sender)
        thread.start()

    # 查询设备信息
    def thread_devStatus(self):
        thread = threading.Thread(target=self.devStatus)
        thread.start()

    # 操作设备
    def thread_all_run(self):
        thread = threading.Thread(target=self.all_run)
        thread.start()
        # self.ui.goButton.setEnabled(False)  # 禁止按钮
        # self.ui.quitButton.setEnabled(False)  # 禁止按钮

    """
        显示线程
    """

    def thread_send_display(self):
        thread = threading.Thread(target=self.send_display)
        thread.start()

    def thread_device_display(self):
        thread = threading.Thread(target=self.device_display)
        thread.start()

    """
        运行
    """

    # 设备信息显示
    def device_display(self):
        self.ui.textBrowser.append(self.device_text)

    # 扫描显示
    def scan_display(self):
        self.ui.textBrowser.append(self.scan_text)

    # 单控显示
    def send_display(self):
        self.ui.textBrowser.append(self.send_text)

    # 清除
    def clear_display(self):
        self.ui.textBrowser.clear()

    # 测试次数
    def test_count(self):
        self.ui.goButton.setEnabled(True)
        self.count = int(self.ui.countEdit.text())
        print(self.count)

    # 退出
    def quit_app(self):
        sys.exit()

    # 组播扫描
    def sender(self):
        self.ui.goButton.setEnabled(True)  # 禁止按钮
        self.ui.quitButton.setEnabled(True)  # 禁止按钮
        # 建立发送socket，和正常UDP数据包没区别
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.local_addr = ('', 4002)
        self.send_sock.bind(self.local_addr)
        cmd_json = {
            "msg": {
                "cmd": "scan",
                "data": {
                    "account_topic": "GA/123456789"
                }
            }
        }
        message = json.dumps(cmd_json)
        self.send_sock.sendto(message.encode(), (self.mcast_group_ip, self.mcast_group_port))
        print("scan\r\n")
        recv_data = self.send_sock.recvfrom(1024)
        recv_msg = recv_data[0]  # 设备信息
        self.send_addr = recv_data[1]  # ip地址
        # self.scan_text = recv_msg.decode("gbk")
        self.scan_text = recv_msg.decode("gbk")  # 字符串
        date = json.loads(self.scan_text)['msg'] ['data']  # json
        for i in date:
            date_key = i
            date_value = date[i]
            self.scan_text = (json.dumps(date_key)+":"+json.dumps(date_value)).replace('"','')
            stats.scan_display()
        # print("%s\r\n" %  recv_msg.decode("gbk"))
        self.ucast_dev_ip = self.send_addr[0]
        time.sleep(2)

    # 查看设备信息
    def devStatus(self):
        # ucast_dev_ip = '192.168.50.117'
        # ucast_dev_port = 4003
        try:
            print("---------ip地址：：：", self.ucast_dev_ip)
            cmd_json = {
                "msg": {
                    "cmd": "devStatus",
                    "data": {
                    }
                }
            }
            message = json.dumps(cmd_json)
            self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
            print("get status\r\n")
            recv_data = self.send_sock.recvfrom(1024)
            recv_msg = recv_data[0]
            send_addr = recv_data[1]
            print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
            self.device_text = recv_msg.decode("gbk")
            stats.thread_device_display()
            time.sleep(2)
        except Exception:
            self.ui.textBrowser.append("先扫描设备！")

    # 单播控制
    def all_run(self):
        count_result = 0
        if self.count == 0:
            self.ui.textBrowser.append("输入测试次数或扫描设备！")
            self.ui.quitButton.setEnabled(True)
            # 启用按钮
        else:
            try:
                while count_result < self.count:
                    self.ui.quitButton.setEnabled(False)
                    self.ui.goButton.setEnabled(False)
                    # 关机
                    cmd_json = {
                        "msg": {
                            "cmd": "turn",
                            "data": {
                                "value": 0
                            }
                        }
                    }

                    message = json.dumps(cmd_json)
                    self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    print(self.ucast_dev_ip + "turn off\r\n")
                    self.send_text = "turn off\r\n"
                    stats.thread_send_display()
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
                    self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    print(self.ucast_dev_ip + "turn on\r\n")
                    self.send_text = "turn on\r\n"
                    stats.thread_send_display()
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
                    self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    print(self.ucast_dev_ip + "set brightness 50\r\n")
                    self.send_text = "set brightness 50\r\n"
                    stats.thread_send_display()
                    time.sleep(2)

                    # # 亮度
                    # cmd_json = {
                    #     "msg": {
                    #         "cmd": "brightness",
                    #         "data": {
                    #             "value": 100
                    #         }
                    #     }
                    # }
                    # message = json.dumps(cmd_json)
                    # self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    # print(self.ucast_dev_ip + "set brightness 100\r\n")
                    # self.send_text = "set brightness 100\r\n"
                    # stats.thread_send_display()
                    # time.sleep(2)

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
                    self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    print(self.ucast_dev_ip + "set red\r\n")
                    self.send_text = "set red\r\n"
                    stats.thread_send_display()
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
                    self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    print(self.ucast_dev_ip + "set green\r\n")
                    self.send_text = "set green\r\n"
                    stats.thread_send_display()
                    time.sleep(2)

                    # 颜色
                    cmd_json = {
                        "msg": {
                            "cmd": "colorwc",
                            "data": {
                                "color": {
                                    "r": 0,
                                    "g": 0,
                                    "b": 255
                                }
                            }
                        }
                    }
                    message = json.dumps(cmd_json)
                    self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    print(self.ucast_dev_ip + "set blue\r\n")
                    self.send_text = "set blue\r\n"
                    stats.thread_send_display()
                    time.sleep(2)

                    # 色温
                    cmd_json = {
                        "msg": {
                            "cmd": "colorwc",
                            "data": {
                                "color": {"r": 245, "g": 243, "b": 255},
                                "colorTemInKelvin": 7000
                            }
                        }
                    }
                    message = json.dumps(cmd_json)
                    self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    print(self.ucast_dev_ip + "set cw 7000\r\n")
                    self.send_text = "set cw 7000\r\n"
                    stats.thread_send_display()
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
                    self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    print(self.ucast_dev_ip + "set cw 3000\r\n")
                    self.send_text = "set cw 3000\r\n"
                    stats.thread_send_display()
                    time.sleep(5)

                    cmd_json = {
                        "msg": {
                            "cmd": "devStatus",
                            "data": {
                            }
                        }
                    }
                    message = json.dumps(cmd_json)
                    self.send_sock.sendto(message.encode(), (self.ucast_dev_ip, self.ucast_dev_port))
                    print("get status\r\n")
                    recv_data = self.send_sock.recvfrom(1024)
                    recv_msg = recv_data[0]
                    send_addr = recv_data[1]
                    print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
                    self.send_text = str(send_addr) + recv_msg.decode("gbk")
                    stats.thread_send_display()
                    time.sleep(2)
                    count_result += 1
                    self.ui.goButton.setEnabled(True)
                    self.ui.quitButton.setEnabled(True)
            except Exception:
                self.ui.textBrowser.append("先扫描设备！")
                self.ui.quitButton.setEnabled(True)


if __name__ == '__main__':
    app = QApplication([])
    stats = App()
    stats.ui.show()
    app.exec_()
