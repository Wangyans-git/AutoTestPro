#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 处理串口数据


import serial

import time
import datetime


class SerialAuto(object):

    def __init__(self, com, dbs, timeout):
        self.err = 0
        self.com = com
        self.dbs = dbs
        self.timeout = timeout
        self.err_date = ''  # 做是否有错误判断的数据
        self.txt_date = ''  # 写入TXT的数据
        self.err_count = 0  # 记录错误次数
        try:
            self.ser = serial.Serial(self.com,
                                     self.dbs,
                                     timeout=self.timeout)
            print("\n*********打开串口成功*********")
        except Exception as e:
            print("\n*********串口异常:{}*********".format(e))
            self.err = -1

    # 写入数据
    def write_date(self, write_itme):
        self.ser.write(write_itme.encode())

    # 读取并处理数据
    def read_date(self):

        check_date = {'开机': '55 10 01 00 01 01 68', '关机': '55 10 01 00 01 00 67', '低档': '55 10 02 00 01 01 69',
                      '中档': '55 10 02 00 01 02 6A',
                      '高挡': '55 10 02 00 01 03 6B', '开启摇头': '55 10 03 00 01 01 6A', '关闭摇头': '55 10 03 00 01 00 69',
                      '风扇档': '55 10 02 00 01 04 6C',
                      '自动挡': '55 10 09 00 01 04 73', '开启童锁': '55 10 05 00 01 01 6C', '关闭童锁': '55 10 05 00 01 00 6B',
                      '关闭显示': '55 10 07 00 01 01 6E',
                      '开启显示': '55 10 07 00 01 00 6D', '绑定温湿度计': 'Govee_ScanBleAdv_Start GAP_CAUSE_SUCCESS',
                      '解绑温湿度计': 'Govee_ScanBleAdv_Stop GAP_CAUSE_SUCCESS'}
        while True:
            now_time = datetime.datetime.now().strftime("\n%Y-%m-%d %H:%M:%S----->")
            is_success_date = ''  # 判断是否执行成功的临时数据
            try:
                date_line = self.ser.readline().decode()
                time.sleep(0.1)
                is_success_date += date_line
                self.txt_date += str(now_time + date_line)  # 所有写入到txt文档
                SerialAuto.write_txt(self.txt_date)
                if check_date['开机'] in is_success_date:
                    success_date = str(now_time) + "开机成功."
                    # self.err_date += success_date
                    self.txt_date += success_date
                    # print(success_date)
                    # break
                    return '开机成功'
                elif check_date['关机'] in is_success_date:
                    success_date1 = str(now_time) + "关机成功."
                    # self.err_date += success_date1
                    self.txt_date += success_date1
                    # print(success_date1)
                    # break
                    return '关机成功'
                elif check_date['低档'] in is_success_date:
                    success_date2 = str(now_time) + '低档成功.'
                    # self.err_date += success_date2
                    self.txt_date += success_date2
                    # print(success_date2)
                    return '设置低档成功'
                elif check_date['中档'] in is_success_date:
                    success_date3 = str(now_time) + '中档成功.'
                    # self.err_date += success_date3
                    self.txt_date += success_date3
                    # print(success_date3)
                    return '设置中档成功'
                elif check_date['高挡'] in is_success_date:
                    success_date4 = str(now_time) + '高档成功.'
                    # self.err_date += success_date4
                    self.txt_date += success_date4
                    # print(success_date4)
                    return '设置高档成功'
                elif check_date['开启摇头'] in is_success_date:
                    success_date5 = str(now_time) + '开摇头成功.'
                    # self.err_date += success_date5
                    self.txt_date += success_date5
                    # print(success_date5)
                    return '开启摇头成功'
                elif check_date['关闭摇头'] in is_success_date:
                    success_date6 = str(now_time) + '关摇头成功.'
                    # self.err_date += success_date6
                    self.txt_date += success_date6
                    # print(success_date6)
                    return '关闭摇头成功'
                elif check_date['开启童锁'] in is_success_date:
                    success_date9 = str(now_time) + '开启童锁成功.'
                    # self.err_date += success_date9
                    self.txt_date += success_date9
                    # print(success_date9)
                    return '开启童锁成功'
                elif check_date['关闭童锁'] in is_success_date:
                    success_date10 = str(now_time) + '关闭童锁成功.'
                    # self.err_date += success_date10
                    self.txt_date += success_date10
                    # print(success_date10)
                    return '关闭童锁成功'
                elif check_date['关闭显示'] in is_success_date:
                    success_date11 = str(now_time) + '关闭显示功能.'
                    # self.err_date += success_date11
                    self.txt_date += success_date11
                    # print(success_date11)
                    return '关闭显示成功'
                elif check_date['开启显示'] in is_success_date:
                    success_date12 = str(now_time) + '开启显示功能.'
                    # self.err_date += success_date12
                    self.txt_date += success_date12
                    # print(success_date12)
                    return '开启显示成功'
                elif check_date['绑定温湿度计'] in is_success_date:
                    success_date13 = str(now_time) + '添加温湿度计成功.'
                    # self.err_date += success_date13
                    self.txt_date += success_date13
                    # print(success_date13)
                    return '绑定温湿度计成功'
                elif check_date['解绑温湿度计'] in is_success_date:
                    success_date14 = str(now_time) + '删除温湿度计成功.'
                    # self.err_date += success_date14
                    self.txt_date += success_date14
                    # print(success_date14)
                    return '解绑温湿度计成功'
                else:
                    continue
            except Exception as e:
                print("获取数据错误!", e)
                break

    # 数据写入txt文档
    @staticmethod
    def write_txt(t):
        result = str(t)
        try:
            with open('log/log.txt', 'w') as file_handle:
                file_handle.write(result)
        except Exception as e:
            print("文件读写出错：", e)

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

program = SerialAuto('com13', 115200, 3)
