#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :yansheng.wang
# @File    :
# @Description : iot test 压测


import datetime
import threading
import time

import serial

from H7124.get_log import GetLog


class SerialAuto(object):

    def __init__(self, com, dbs, timeout):
        self.err = 0
        self.com = com
        self.dbs = dbs
        self.timeout = timeout
        self.err_date = ''  # 做是否有错误判断的数据
        self.txt_date = ''  # 写入TXT的数据
        self.err_count = 0  # 记录错误次数
        self.get_log = GetLog(f"iot log\\log.txt")
        try:
            self.ser = serial.Serial(self.com,
                                     self.dbs,
                                     timeout=self.timeout)
            print("*********打开串口成功*********")
        except Exception as e:
            print("*********串口异常:{}*********".format(e))
            self.err = -1

    # 写入数据
    def write_date(self, write_itme):
        self.ser.write(write_itme.encode())

    # 读取处理数据
    def read_date(self, check_date):
        check_dates = {}  # 断言数据
        while True:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S----->")
            is_success_date = ''  # 判断是否执行成功的临时数据
            try:
                date_line = self.ser.readline().decode()
                # time.sleep(0.1)
                is_success_date += date_line
                self.txt_date += str(date_line)  # 所有写入到txt文档
                # print(self.txt_date)
                self.write_txt(self.txt_date)
                # self.logs.info(self.txt_date)
                for i in range(len(check_date)):
                    # 开机:55 01 01 57,关机:55 01 00 56
                    check_dates[check_date[i].split(":")[0]] = check_date[i].split(":")[1]  # 将每个输入的键值对加入到字典里
                    check_list = []
                    for j in check_dates:
                        check_list.append(j)
                    if check_dates[check_list[i]] in date_line:
                        success_date = str(now_time + check_list[i]) + "成功"
                        print(success_date)
                        self.get_log.info(success_date)
                        self.err_date += success_date
                        self.txt_date += success_date
            except Exception as e:
                print(e)

    # 判断错误数据
    def date_result(self, n):
        date = self.err_date.split('成功')
        if len(date) - 2 == len(n):  # 因为split分隔后会多一段数据，所以-1
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
            self.get_log.error(err_)
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
    def thread_recv(self, d):
        try:
            thread = threading.Thread(target=self.read_date, args=(d,), daemon=True)
            thread.start()
        except Exception as e:
            print("无法启动线程:{}".format(e))

    def run_test(self):
        m = 0  # 统计测试次数
        program.write_date("iHoment_20170201\r")
        time.sleep(1)
        program.write_date("log print 0\r")
        while True:
            print("========第{}次测试开始========".format(m + 1))
            self.get_log.info("========第{}次测试开始========".format(m + 1))
            for i in range(len(send_list)):
                program.write_date(send_list[i])  # 写入数据
                self.get_log.info("输入{0}".format(send_list[i]))
                print("输入{0}".format(send_list[i]))
                time.sleep(2)
            print("========第{}次测试完成========".format(m + 1))
            self.get_log.info("========第{}次测试完成========".format(m + 1))
            # program.date_result(send_list)
            m += 1



if __name__ == '__main__':
    program = SerialAuto('com17', 115200, 3)

    # check_dates = ['关机:55 01 00 56', '开机:55 01 01 57']
    check_list = (
        '开机:55 15 01 00 01 01 6D,'
        '小冰:55 15 02 00 01 01 6E,中冰:55 15 02 00 01 02 6F,大冰:55 15 02 00 01 03 70,'
        '蜂鸣器关:55 15 06 00 01 00 71,蜂鸣器开:55 15 06 00 01 01 72,'
        '勿扰开:55 15 22 00 01 01 8E,勿扰关:55 15 22 00 01 00 8D,'
        '预约定时开:55 15 19 00 01 01 85,预约定时关:55 15 19 00 01 00 84,'
        '关机:55 15 01 00 01 00 6C,'
        '清洁开:55 15 18 00 01 01 84,清洁关:55 15 18 00 01 00 83'
    )
    check_dates = check_list.upper().split(",")
    # print(check_dates)
    # 如果
    if program.err == 0:
        # test_count = int(input("输入需要测试的次数："))  # 测试的次数
        print("*********开启输入iot指令*********\r")
        program.thread_recv(check_dates)
        send_list = [
            'iot_test 01 01\r',  # 开机
            'iot_test 02 01\r', 'iot_test 02 02\r', 'iot_test 02 03\r',  # 冰
            'iot_test 06 00\r', 'iot_test 06 01\r',  # 蜂鸣器开关
            'iot_test 22 01\r', 'iot_test 22 00\r',  # 勿扰
            'iot_test 19 01\r', 'iot_test 19 00\r',  # 预约定时
            'iot_test 01 00\r',
            'iot_test 18 01\r', 'iot_test 18 00\r'  # 清洁
        ]  # 关机
        program.run_test()
