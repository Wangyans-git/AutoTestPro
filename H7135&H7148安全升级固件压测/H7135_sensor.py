#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :yansheng.wang
# @File    :
# @Description : OTA次数统计

import os
import time
from datetime import datetime

import openpyxl
import serial

from H7135.logs.get_log import GetLog

log_name = datetime.now().strftime("logs\\iot_test_%Y%m%d_%H%M%S.txt")
time_log = datetime.now().strftime("_%Y%m%d_%H%M%S.txt")


class H7135_OTA(object):

    def __init__(self, com, dbs, timeout):
        self.com = com
        self.dbs = dbs
        self.timeout = timeout
        self.get_log = GetLog(f"logs\\发送_log.txt")
        try:
            self.ser = serial.Serial(self.com,
                                     self.dbs,
                                     timeout=self.timeout)
            print("*********打开串口成功*********")
        except Exception as e:

            print("*********串口异常:{}*********".format(e))

    # 读取处理数据
    def sensor_num(self):

        sensor_count = 0
        while True:
            try:
                self.ser.write(bytes.fromhex('A0 01 01 A2'))
                time.sleep(0.5)
                self.ser.write(bytes.fromhex('A0 01 00 A1'))
                sensor_count += 1
            except Exception as e:
                print(e)
                pass
            print(f"发送sensor广播次数:{sensor_count}次")

            self.get_log.info(f"发送sensor广播次数:{sensor_count}次")
            time.sleep(2)



if __name__ == '__main__':
    program = H7135_OTA('com4', 9600, 3)
    program.sensor_num()
