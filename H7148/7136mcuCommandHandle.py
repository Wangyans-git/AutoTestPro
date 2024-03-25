#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/20 18:43
@Author  : jhcheng
@FileName: mcuCommandHandle.py
@SoftWare: PyCharm
"""
import serial
import os
from time import sleep
import binascii
import time
import threading
import random
import logging


class McuCommandHandle():
    dataList = ''
    lock = threading.Lock()

    def __init__(self, mcu_command, device_name, times, com, bps, timeout, com2, bps2, bytesize, stopbits, Ret1, Ret2):
        self.mcu_command = mcu_command
        self.device = device_name
        self.Ret1 = Ret1
        self.Ret2 = Ret2
        self.times = times

        # 打印串口
        self.port = com
        self.bps = bps
        self.timeout = timeout
        self.start = True
        try:
            # 打开串口，并得到串口对象
            self.main_engine = serial.Serial(self.port, self.bps, timeout=self.timeout)
            self.main_engine.flushInput()  # 清空缓冲区
            # 判断是否打开成功
            if (self.main_engine.is_open):
                self.Ret1 = True
                # 日志
                self.loger = self.get_loger(self.device)
        except Exception as e:
            print("---异常---：", e)

    def run(self):
        if (self.Ret1):
            threading.Thread(target=ms.send_mcu_with_check_handle, ).start()
            threading.Thread(target=ms.recv, ).start()
            # self.relay_off()
        else:
            print("创建串口失败")

    # 设备断电上电再发送mcu指令
    # def on_off_send_mcu_handle(self, times):
    #     n = 0  # 统计
    #     # 主循环
    #     for i in range(times):
    #         self.relay_h.on()
    #         print('设备上电')
    #         self.loger.info('设备上电')
    #         sleep(3)
    #         self.send_data('govee')  # 登录串口
    #         sleep(1)
    #         self.send_data('log print 0')  # 关闭所有日志
    #         sleep(0.5)
    #         self.send_data('log enable mcu')  # 打开mcu日志
    #         sleep(0.5)
    #         self.send_data(self.mcu_command[1])  # 设备开机
    #         sleep(1)
    #         result = self.log_check(self.dataList, 'on', recv_command[1])  # 检测串口数据
    #         if result:
    #             n += 1
    #             print('开机成功')
    #             self.loger.info('开机成功')
    #             sleep(1)
    #         else:
    #             print('开机失败')
    #             self.loger.info('开机失败')
    #
    #         # 切换二档
    #         self.send_data(self.mcu_command[3])
    #         # 检测串口数据
    #         sleep(1)
    #         result = self.log_check(self.dataList, 'other', recv_command[3])
    #         if result:
    #             n += 1
    #             print('二档切换成功')
    #             self.loger.info('二档切换成功')
    #             sleep(1)
    #         else:
    #             print('二档切换失败')
    #             self.loger.info('二档切换失败')
    #
    #         # 切换三档
    #         self.send_data(self.mcu_command[4])
    #         # 检测串口数据
    #         sleep(1)
    #         result = self.log_check(self.dataList, 'other', recv_command[4])
    #         if result:
    #             n += 1
    #             print('三档切换成功')
    #             self.loger.info('三档切换成功')
    #             sleep(1)
    #         else:
    #             print('三档切换失败')
    #             self.loger.info('三档切换失败')
    #
    #         self.relay_h.off()
    #         print('设备断电')
    #         self.loger.info('设备断电')
    #         sleep(3)
    #
    #         print('第[%s]次循环结束。' % (i + 1))
    #         self.loger.info('第[%s]次循环结束。' % (i + 1))
    #     print('设备[%s]' % self.device + '断电上电[%s]次' % times + '，指令压测[%s]次，' % (times * 3) + '成功了[%s]次.' % n)
    #     self.loger.info('设备[%s]' % self.device + '断电上电[%s]次' % times + '，指令压测[%s]次，' % (times * 3) + '成功了[%s]次.' % n)

    # 单纯发送mcu指令
    def send_mcu_with_check_handle(self):
        # sleep(5)
        success = 0
        fail = 0
        count1 = 0
        count2 = 0
        while True:
            # 发送有效数据
            if random.randint(0, 1) % 2 == 0:
                # 发送数据
                value_index = random.randint(0, len(self.mcu_command) - 1)
                self.value_data = self.mcu_command[value_index]
                print('发送有效数据%s:' % self.value_data)
                self.loger.info('发送有效数据%s:' % self.value_data)
                self.send_data_hex(self.value_data)
                # 检测串口数据
                time.sleep(0.03)
                # self.sleep_with_fractional_seconds(0.2)
                if count1 == 0:
                    print('第一次发送不处理')
                else:
                    result = self.log_check(self.dataList, 'other', recv_command[value_index].lower())
                    if result == 1:
                        success += 1
                    elif result == 0:
                        fail += 1
                        print('----------------------------------返回值校验失败-------------------------------------')
                        self.loger.info(
                            '----------------------------------返回值校验失败-------------------------------------')
                    else:
                        fail += 1
                        print('--------------------------')
                        # self.loger.info('-------------返回值校验失败-------------')
                count1 += 1
                print('设备[%s]' % self.device + '有效指令压测[%s]次，' % (
                            count1 - 1) + '成功了[%s]次，' % success + '失败了[%s]次，' % (count1-success-1) +
                      '无效指令发送了%s次' % count2)
                print('-----------------------------------------------------')
                # self.loger.info(
                #     '设备[%s]' % self.device + '有效指令压测[%s]次，' % (count1 - 1) + '成功了[%s]次.' % success +
                #     '无效指令发送了%s次' % count2)
                # self.loger.info('-----------------------------------------------------')
            else:
                pass
                # invalue_index = random.randint(0, len(invalue_command) - 1)
                # invalue_date = invalue_command[invalue_index]
                # print('发送无效数据%s:' % invalue_date)
                # # self.loger.info('发送无效数据%s:' % invalue_date)
                # self.send_data_hex(invalue_date)
                # count2 += 1

    # 纯发送指令，不校验结果
    # def send_mcu_no_check_handle(self):
    #     sleep(3)
    #     n = 0
    #     while True:
    #         try:
    #             data = mcu_command[random.randint(0, len(mcu_command) - 1)]
    #             self.send_data_hex(data)
    #             print('send data ---------%s-----------:' % n + str(data))
    #             # self.loger.info('send data ---------%s-----------:' % n + str(data))
    #             sleep(3)
    #             n += 1
    #         except Exception as e:
    #             print(e)

    # 发送mcu指令数据
    def send_data(self, data):
        # 输入密码
        self.main_engine.write(data.encode('utf-8'))
        # 输入回车确认
        self.main_engine.write(chr(0xD).encode())

    # 发十六进制数据
    def send_data_hex(self, data):
        self.main_engine.write(bytes.fromhex(data))

    # 串口校验
    def log_check(self, dataList, option_type, sl):
        substrings_to_remove = ['aa050000af', 'aa050000', 'aa0500', "aa05"]
        dataList_rep = dataList
        for sub in substrings_to_remove:
            dataList_rep = dataList_rep.replace(sub, "")
        # print(dataList_rep)  # 输出: 9b0019b
        if option_type == 'on':
            start = len(dataList_rep) - 200
        # elif len(self.value_data) == 11:
        #     start = len(dataList_rep) - 10
        # elif len(self.value_data) == 113:
        #     start = len(dataList_rep) - 76
        # elif len(self.value_data) == 41:
        #     start = len(dataList_rep) - 28
        else:
            start = len(dataList_rep) - 12
            # print(dataList)
        end = len(dataList_rep)
        str1 = dataList_rep[start:end]
        # print("============",str1)
        # print("--------------------------------------------------------------------------------------------------------------------------",str1)
        # str1 = dataList[:end]
        str2 = str1.replace(" ", "").replace("\r", "").replace("\n", "")  # 去掉空格、回车符、换行符
        print("str2", str2)
        # strlist = str2.split(':', 2)  # 以冒号进行分割
        if str(str2).find('aa') >= 0:
            strlist = str2.split('aa', 2)  # 以55进行分割
            print('strlist:', strlist)
            if strlist[1] == '':
                strlist = 'aa' + str(strlist[0])
            else:
                strlist = 'aa' + str(strlist[1])
            # strlist = 'aa' + str(strlist[1])
            # 打印串口日志
            self.loger.info('本次操作后MCU返回日志：' + str(strlist))
            print('本次操作后MCU返回日志：' + str(strlist))
            # time.sleep(0.1)
            # print(str(strlist).find(sl))
            # if str(strlist).find(sl) >= 0:
            # print(strlist)

            if sl in str(strlist):
                return 1
            else:
                return 0
        else:
            print('本次操作后mcu没有回---------------------')
            # self.loger.info('本次操作后mcu没有回------------------')
            return 2

    # 监测串口日志
    # def com_log_check(self, dataList, option_type, sl):
    #     if option_type == 'on':
    #         start = len(dataList) - 900
    #     elif option_type == 'off':
    #         start = len(dataList) - 1600
    #     else:
    #         start = len(dataList) - 520
    #     end = len(dataList)
    #     str1 = dataList[start:end]
    #     str2 = str1.replace(" ", "").replace("\r", "").replace("\n", "")  # 去掉空格、回车符、换行符
    #     strlist = str2.split(':', 50)  # 以冒号进行分割
    #     # 打印串口日志
    #     self.loger.info('本次操作后蓝牙日志：' + str(strlist))
    #     print('本次操作后蓝牙日志：' + str(strlist))
    #     if str(strlist).find(sl) >= 0:
    #         print('操作成功')
    #         self.loger.info('操作成功')
    #         return True
    #     elif str(strlist).find('DEV_CMD_ONOFF') >= 0 and option_type == 'on':
    #         print('设备本来是开，无法操作')
    #         self.loger.info('设备本来是开，无法操作')
    #     elif str(strlist).find('DEV_CMD_ONOFF') >= 0 and option_type == 'off':
    #         print('设备本来是关，无法操作')
    #         self.loger.info('设备本来是关，无法操作')
    #     else:
    #         print('操作失败')
    #         self.loger.info('操作失败')
    #         return False

    # 接收串口十六进制数据
    def recv(self):
        if self.start:
            print("开始接收数据：")
        else:
            print("测试完毕，停止接收数据：")
        while self.start:

            try:
                count = self.main_engine.inWaiting()  # 获取串口缓冲区数据
                # print("count:",count)
                if count != 0:
                    # data = self.main_engine.read(self.main_engine.in_waiting).decode("gbk")  # 读出串口数据，数据采用gbk编码
                    # predata = self.main_engine.read(self.main_engine.in_waiting)
                    # predata = self.main_engine.readline(self.main_engine.in_waiting)
                    predata = self.main_engine.readline(count)

                    # 读取串口接卸数据（由bytes数据类型转换为hex16进制数据类型，转成str，再去掉开头b'与结尾'）
                    data = str(binascii.b2a_hex(predata))[2:-1]

                    # print("predata:", data)
                    # data = binascii.a2b_hex(predata).decode()
                    # print(time.strftime("%Y-%m-%d %H-%M-%S"), " --- recv --> ")  # 打印一下子
                    # time.sleep(0.01)  # 延时0.1秒，免得CPU出问题
                    self.dataList += data

                    # print(self.dataList)
                    # time.sleep(3)

                    # print('predata:' + str(predata))
                    # print('data:'+str(data))
            except Exception as e:
                print("异常报错：", e)

    def get_loger(self, logfile_name):
        if os.path.exists('d:'):
            LOG_BASE_DIR = 'D:/'
        else:
            LOG_BASE_DIR = 'C:/'
            # 日志目录
        log_path = os.path.join(LOG_BASE_DIR, "logs", "pylog").replace('\\', '/')
        isExists = os.path.exists(log_path)
        if not isExists:  # 判断如果文件不存在,则创建
            os.makedirs(log_path)
            print("目录创建成功")
        else:
            print("目录已经存在")
        now = time.strftime("%Y-%m-%d %H-%M-%S")
        self.log_name = log_path + '/' + now + "_" + logfile_name + "_日志.txt"
        self.logger = logging.getLogger()  # 日志对象
        self.logger.setLevel(logging.DEBUG)  # 设置日志等级
        self.file_handler = logging.FileHandler(self.log_name, 'a', 'utf-8')
        self.file_handler.setLevel(logging.INFO)
        formater = logging.Formatter(
            '%(asctime)s %(filename)s---> %(threadName)s %(levelname)s %(module)s %(funcName)s---> %(message)s')
        self.file_handler.setFormatter(formater)
        self.logger.addHandler(self.file_handler)
        return self.logger

    def sleep_with_fractional_seconds(self, seconds):
        whole_seconds = int(seconds)  # 获取整数部分
        fractional_seconds = seconds - whole_seconds  # 获取小数部分

        # 等待整数秒
        time.sleep(whole_seconds)

        # 等待小数秒（使用 threading.Timer）
        t = threading.Timer(fractional_seconds, lambda: None)
        t.start()
        t.join()


if __name__ == '__main__':
    device_name = 'H7136'  # 设备名称
    times = 2000  # 测试次数
    com = "com4"  # 串口编号
    # bps = 115200  # 波特率
    bps = 19200
    timeout = 0.5  # 串口超时
    com2 = 'com12'
    bps2 = 9600
    bytesize = 8
    stopbits = 1
    Ret1 = False  # 日志串口是否创建成功标志
    Ret2 = False  # 继电器串口是否创建成功标志

    # # 输入指令
    # mcu_command = ['iot_test 01 00', 'iot_test 01 01',
    #                'iot_test 02 01', 'iot_test 02 02', 'iot_test 02 03',
    #                'iot_test 03 00', 'iot_test 03 01',
    #                'iot_test 05 00', 'iot_test 05 01',
    #                'iot_test 06 00', 'iot_test 06 01',
    #                'iot_test 07 00', 'iot_test 07 01']
    #
    # # 回复指令
    # recv_command = ['AA1001000100BC', 'AA1001000101BD',
    #                 'AA1002000101BE', 'AA1002000102BF', 'AA1002000103C0',
    #                 'AA1003000100BE', 'AA1003000101BF',
    #                 'AA1005000100C0', 'AA1005000101C1',
    #                 'AA1006000100C1', 'AA1006000101C2',
    #                 'AA1007000100C2', 'AA1007000101C3'
    #                 ]
    invalue_command = ['55 F0 01 38', '55 F7 02 12', '55 02 56 03 5A', '56 02 01 FF 57', 'AA 02 07 FF 5D']

    mcu_command = [
        '55 F0 01 46',  # 心跳
        '55 F7 01 4d',  # 软件版本
        '55 F7 02 4e',  # 硬件版本
        # '55 02 00 01 58', '55 02 00 03 5A', '55 02 00 07 5E', '55 02 00 0F 66', '55 02 00 1F 76', '55 02 00 3F 96',
        # '55 02 00 7F D6', '55 02 00 FF 56', '55 02 01 FF 57', '55 02 03 FF 59', '55 02 07 FF 5D',  # 指示灯
        # '55 03 04 02 01 01 05 6B'
    ]

    recv_command = [
        'aaf0019b',
        'aaf7810224',
        'aaf7415032',
        # 'aa020001ad', 'aa020003af', 'aa020007b3', 'aa02000fbb', 'aa02001fcb', 'aa02003feb',
        # 'aa02007f2b', 'aa0200ffab',
        # 'aa0201ffac', 'aa0203ffae', 'aa0207ffb2'
    ]
    ms = McuCommandHandle(mcu_command, device_name, times, com, bps, timeout, com2, bps2, bytesize, stopbits, Ret1,
                          Ret2)
    ms.run()
