#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 压力测试
import time
from datetime import datetime

import serial
import serial.tools.list_ports
import uiautomator2 as u2

from Pressure_test.logs import get_log

log_name = datetime.now().strftime("logs\\压测结果_%Y%m%d_%H%M%S.txt")


class PressureTest:

    def __init__(self, com, com1, dbs, dbs1, timeout):
        self.device = u2.connect("192.168.50.237")
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        # self.device.settings['operation_delay'] = (1, 1)  # 每次点击后等待2s
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        # 脚本日志
        self.get_log = get_log.GetLog(log_name)
        self.in_page_num = 0
        # self.device.unlock()  # 解锁屏幕
        try:
            self.ser = serial.Serial(com,
                                     dbs,
                                     timeout=timeout)
            self.relay_ser = serial.Serial(com1,  # 继电器
                                           dbs1,
                                           timeout=timeout)
            print("*********打开串口成功*********")
        except Exception as e:
            print("*********串口异常:{}*********".format(e))
            self.err = -1

    # ble压测
    def in_page(self, sku_list):
        for in_sku in sku_list:
            while True:
                try:
                    self.device(text=in_sku).click_exists(timeout=5)
                    old_time = datetime.now()
                    if self.device(resourceId='com.govee.home:id/iv_switch').exists(timeout=30):
                        new_time = datetime.now()
                        self.in_page_num += 1
                        in_time = new_time - old_time
                        self.get_log.info(
                            "{0} ble进入详情页用时：[{1}][第{2}次]".format(in_sku, in_time, self.in_page_num))
                        print("{0} ble进入详情页用时：[{1}][第{2}次]".format(in_sku, in_time, self.in_page_num))
                        if self.device(resourceId='com.govee.home:id/iv_back').exists(timeout=5):
                            self.device(resourceId='com.govee.home:id/iv_back').click_exists(timeout=5)
                        if self.device(resourceId='com.govee.home:id/btn_back').exists(timeout=5):
                            self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=5)
                        time.sleep(5)
                        # if self.in_page_num == 1000:
                        #     print("测试结束")
                        #     break
                    else:
                        while True:
                            self.device(text=in_sku).click_exists(timeout=5.0)
                            if self.enter_device(in_sku):
                                break
                            else:
                                time.sleep(5)
                    # self.get_log.info("第{0}次".format(self.in_page_num))
                except Exception:
                    pass

    # 开关压测
    def on_off_test(self, on_off_list):
        on_off_num = 0
        for i in on_off_list:
            print(i)
            self.device(text=i).click_exists(timeout=10)
            while True:
                try:
                    # self.ser.write(bytes.fromhex('A0 01 01 A2'))
                    # time.sleep(1)
                    # self.ser.write(bytes.fromhex('A0 01 00 A1'))
                    # time.sleep(3)
                    # self.ser.write(bytes.fromhex('A0 01 01 A2'))
                    # time.sleep(1)
                    # self.ser.write(bytes.fromhex('A0 01 00 A1'))
                    if self.device(text="重新连接").exists():
                        self.device(text="重新连接").click_exists(timeout=5)
                    flag = self.device(resourceId='com.govee.home:id/iv_auto_icon').info['enabled']
                    if not flag:
                        on_off_num += 1
                        self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5)
                        print("{0}开关测试次数：{1}".format(i, on_off_num))
                        self.get_log.info("{0}开关测试次数：{1}".format(i, on_off_num))
                    # if on_off_num == 1000:
                    #     self.get_log.info("测试结束")
                    #     self.device(resourceId='com.govee.home:id/iv_back').click_exists(timeout=30)
                    #     on_off_num = 0
                    #     time.sleep(5)
                    #     break
                except Exception as e:
                    print(e)
                time.sleep(10)

    # ota压测
    def ota_test(self):
        time_start = 0
        ota_num = 0
        time_end = 0
        while True:
            try:
                date_line = self.ser.readline().decode()
                # time.sleep(0.1)
                print(date_line)
                # self.write_txt(self.txt_date)
                while True:
                    if '"percent":"0"' in date_line:
                        time.sleep(time_start + 0.02)  # 每次断电间隔时间加0.02s
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                        print("设备在开始OTA下载后{0}秒断电".format(time_start))
                        self.get_log.info("设备在开始OTA下载后{0}秒断电".format(time_start))
                        time.sleep(3)
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                        print("停止时间：{0}".format(time_start))
                        ota_num += 1
                        print('"设备在开始OTA下载后断电{0}次"'.format(ota_num))
                        self.get_log.info('"设备在开始OTA下载后断电{0}次"'.format(ota_num))
                    elif '"percent":"100"' in date_line:
                        time.sleep(0.1)
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                        time.sleep(3)
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                        ota_num += 1
                        break
                    else:
                        break
                if ota_num == 1000:
                    print("测试结束")
                    break
            except Exception as e:
                print(e)

    # 恢复出厂压测
    def factory_test(self):
        factory_num = 0
        while True:
            try:
                self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                time.sleep(10)
                self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                time.sleep(30)
                factory_num += 1
                print("恢复出厂测试次数：", factory_num)
                self.get_log.info("恢复出厂测试次数：{0}".format(factory_num))
                if factory_num == 1000:
                    self.get_log.info("测试结束")
                    break
            except Exception:
                pass

    # 进入详情页验证
    def enter_device(self, sku=None):
        if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=30):
            print("进入详情页")
            self.in_page_num += 1
            self.get_log.info("进入{0}详情页成功".format(sku))
            return True
        else:
            # 退出详情页
            try:
                if self.device(resourceId='com.govee.home:id/iv_back').exists(timeout=5):
                    self.device(resourceId='com.govee.home:id/iv_back').click_exists(timeout=5)
                if self.device(resourceId='com.govee.home:id/btn_back').exists(timeout=5):
                    self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=5)
                print("{0}30秒还未进入详情页，连接设备失败，退出详情页".format(sku))
                self.get_log.info("{0}30秒还未进入详情页，连接设备失败，退出详情页".format(sku))
            except Exception as e:
                print(e)
            return False

    def down(self):
        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                          0.1 * self.height)  # 向下滑动


"""
packaging.version.InvalidVersion: Invalid version: ''    提示这个就是手机没打开ATX服务
"""
if __name__ == '__main__':
    run = PressureTest('com9', 'com7', 115200, 9600, 1)  # com为串口日志，com1为继电器
    # test_list = ['Smart Plug Pro8', 'Smart Plug Pro4', 'Smart Plug Pro5', 'Smart Plug Pro3', 'Smart Plug Pro1']   #
    test_list = ['H7148断电上电开机压测']  #
    # run.in_page(test_list)  # ble压测
    # run.factory_test()   # 恢复出厂压测
    run.on_off_test(test_list)  # 开关机压测
    # run.ota_test()  # 开关机压测
