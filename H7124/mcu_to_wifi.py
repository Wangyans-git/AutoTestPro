#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : mcu和wifi通信


import serial
import threading
import time
import datetime


class SerialAuto(object):

    # def __init__(self, com, dbs, com1, dbs1, com2, dbs2,timeout):
    def __init__(self,  com1, dbs1, com2, dbs2,timeout):
        self.err = 0
        # self.com = com
        # self.dbs = dbs
        self.timeout = timeout
        self.err_date = ''  # 做是否有错误判断的数据
        self.txt_date = ''  # 写入TXT的数据
        self.err_count = 0  # 记录错误次数
        try:
            # self.ser = serial.Serial(com,
            #                          dbs,
            #                          timeout=timeout)
            self.relay_ser = serial.Serial(com1,  # 继电器
                                           dbs1,
                                           timeout=timeout)
            self.relay_ser1 = serial.Serial(com2,  # 继电器1
                                           dbs2,
                                           timeout=timeout)
            print("*********打开串口成功*********")
        except Exception as e:
            print("*********串口异常:{}*********".format(e))
            self.err = -1

    # 写入数据
    def write_date(self, write_itme):
        self.ser.write(write_itme.encode('UTF-8'))
        self.ser.write('\r'.encode())

    # 读取处理数据
    def read_date(self, check_date):
        check_edit = check_date
        check_dates = {}  # 断言数据
        while True:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S----->")
            is_success_date = ''  # 判断是否执行成功的临时数据
            # try:
            date_line = self.ser.readline().decode()
            # time.sleep(0.1)
            is_success_date += date_line
            # print(is_success_date)
            self.txt_date += str(date_line)  # 所有写入到txt文档
            self.write_txt(self.txt_date)
            for i in range(len(check_edit)):
                # 开机:55 11 01 00 01 01 69, 关机:55 11 01 00 01 00 68
                check_dates[check_edit[i].split(":")[0]] = check_edit[i].split(":")[1]  # 将每个输入的键值对加入到字典里
                check_list = []
                for j in check_dates:
                    check_list.append(j)
                if check_dates[check_list[i]] in date_line:
                    print(check_dates[check_list[i]])
                    # success_date = str(now_time + check_list[i]) + "."
                    success_date = str(now_time + check_list[i])
                    print("{}".format(success_date))
                    self.err_date += success_date
                    self.txt_date += success_date
            # except Exception as e:
            #     print(e)

    # 判断错误数据
    def date_result(self, n):
        date = self.err_date.split('.')
        if len(date) - 1 == len(n):  # 因为split分隔后会多一段数据，所以-1
            for j in date:
                # print(j)
                pass  # 存入txt文档
            self.err_date = ''
        elif len(date) == 1:
            pass
        else:
            err_ = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S前的一次执行中有错误！！！"))
            self.txt_date += err_
            SerialAuto.write_txt(self.txt_date)
            print(err_)
            self.err_date = ''
            self.err_count += 1
        return self.err_count

    # 数据写入txt文档
    @staticmethod
    def write_txt(t):
        result = str(t)
        try:
            with open('log.txt', 'w') as file_handle:
                file_handle.write(result)
        except Exception as e:
            print("文件读写出错：", e)

    # 线程读取数据
    # def thread_recv(self, d):
    def thread_recv(self):
        try:
            # thread = threading.Thread(target=self.read_date, args=(d,))
            thread1 = threading.Thread(target=self.relay)
            # thread.start()
            thread1.start()
        except Exception as e:
            print("无法启动线程:{}".format(e))

    # 开关
    def relay(self):
        m = 0  # 统计测试次数
        while True:
            self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
            time.sleep(0.4)
            self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
            time.sleep(0.4)
            self.mode_relay()
            self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
            time.sleep(0.4)
            self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
            time.sleep(0.4)
            m += 1

    # 档位
    def mode_relay(self):
        for i in range(5):
            self.relay_ser1.write(bytes.fromhex('A0 01 01 A2'))
            time.sleep(0.4)
            self.relay_ser1.write(bytes.fromhex('A0 01 00 A1'))
            time.sleep(0.4)


if __name__ == '__main__':
    # program = SerialAuto('com13', 115200, 'com8', 9600, 'com9', 9600,3)
    program = SerialAuto('com15', 9600, 'com16', 9600,3)
    check_dates = [
        "一档:55 02 00 03 5A", "二档:55 02 00 05 5C", "三档:55 02 00 09 60", "自动档:55 02 00 11 68","风扇档:55 02 00 21 78",
        "关机:55 02 00 01 58",
        "1H:55 02 00 83 DA","2H:55 02 01 03 5B","3H:55 02 03 83 DD","4H:55 02 02 03 5C","5H:55 02 02 83 DC","6H:55 02 03 03 5D","7H:55 02 03 83 DD"
    ]
    # 如果
    if program.err == 0:
        print("*********开启测试*********\r")
        program.thread_recv()
