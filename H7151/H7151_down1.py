#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 单机压测
import threading
import time
import random

import serial
import uiautomator2 as u2

from H7142.get_log.get_log import GetLog


class H7151Test:
    def __init__(self):
        # self.device = u2.connect_usb('d5cd8968')
        self.device = u2.connect_usb('YDHUE6Q4GAAQCYCY')
        self.device.app_start('com.govee.home')
        # self.device.implicitly_wait(30)  # 元素等待时间30s
        self.device.settings['wait_timeout'] = 10  # 元素等待时间30s
        # self.device.settings['operation_delay'] = 1  # 每次点击后等待1s
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\H7135_Auto\get_log\H7135_log.log")

        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H7151'

    def start_test(self):
        # 判断当前是否需要进入详情页
        try:
            self.ser = serial.Serial("com8",
                                     9600,
                                     timeout=1)
        except Exception as e:
            print("没有可用串口了", e)
        if self.device(text=self.sku).wait(timeout=5.0):
            self.device(text=self.sku).click_exists(timeout=5.0)
            time.sleep(5)
            n = 0
            if self.check_connect():
                while True:
                    try:
                        # self.logs.info('退出详情页')
                        if n % 3 == 0:
                            if self.device(text="重新连接").exists():
                                self.device(text="重新连接").click_exists(timeout=10)
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/iv_gear_low_icon').click_exists(timeout=5.0)
                            self.get_log.info("低档")
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.gear()
                            time.sleep(1)
                            self.ser.write(bytes.fromhex('A0 01 01 A2'))
                            time.sleep(1)
                            self.ser.write(bytes.fromhex('A0 01 00 A1'))
                            time.sleep(5)
                            self.ser.write(bytes.fromhex('A0 01 01 A2'))
                            time.sleep(1)
                            self.ser.write(bytes.fromhex('A0 01 00 A1'))
                            time.sleep(30)
                            n += 1
                        elif n % 3 == 1:
                            if self.device(text="重新连接").exists():
                                self.device(text="重新连接").click_exists(timeout=10)
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').click_exists(timeout=5.0)
                            self.get_log.info("中档")
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.gear()
                            time.sleep(2)
                            self.ser.write(bytes.fromhex('A0 01 01 A2'))
                            time.sleep(1)
                            self.ser.write(bytes.fromhex('A0 01 00 A1'))
                            time.sleep(5)
                            self.ser.write(bytes.fromhex('A0 01 01 A2'))
                            time.sleep(1)
                            self.ser.write(bytes.fromhex('A0 01 00 A1'))
                            time.sleep(30)
                            n += 1
                        elif n % 3 == 2:
                            if self.device(text="重新连接").exists():
                                self.device(text="重新连接").click_exists(timeout=10)
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/iv_gear_high_icon').click_exists(timeout=5.0)
                            self.get_log.info("高档")
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.gear()
                            time.sleep(3)
                            self.ser.write(bytes.fromhex('A0 01 01 A2'))
                            time.sleep(1)
                            self.ser.write(bytes.fromhex('A0 01 00 A1'))
                            time.sleep(5)
                            self.ser.write(bytes.fromhex('A0 01 01 A2'))
                            time.sleep(1)
                            self.ser.write(bytes.fromhex('A0 01 00 A1'))
                            time.sleep(30)
                            n += 1
                        elif n % 3 == 3:
                            if self.device(text="重新连接").exists():
                                self.device(text="重新连接").click_exists(timeout=10)
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/iv_dry_clothes_icon').click_exists(timeout=5.0)
                            self.get_log.info("干衣档")
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.gear()
                            time.sleep(4)
                            self.ser.write(bytes.fromhex('A0 01 01 A2'))
                            time.sleep(1)
                            self.ser.write(bytes.fromhex('A0 01 00 A1'))
                            time.sleep(5)
                            self.ser.write(bytes.fromhex('A0 01 01 A2'))
                            time.sleep(1)
                            self.ser.write(bytes.fromhex('A0 01 00 A1'))
                            time.sleep(30)
                            n += 1
                    except Exception as e:
                        print(e)
                    print("已经测试了{}次".format(n))
            else:
                while True:
                    self.device(text=self.sku).click_exists(timeout=5.0)
                    if self.check_connect():
                        break
                    else:
                        time.sleep(5)
        else:
            print("没有改找到该设备名的设备!")

    def gear(self):
        self.device.click(0.239, 0.84)  # 1档
        self.pop()
        self.device.click(0.765, 0.84)  # 5档
        self.pop()

    def pop(self):
        if self.device(resourceId='com.govee.home:id/btn_done').exists():
            self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=5.0)

    # 小数点暂停
    def sleep_with_fractional_seconds(self, seconds):
        whole_seconds = int(seconds)  # 获取整数部分
        fractional_seconds = seconds - whole_seconds  # 获取小数部分

        # 等待整数秒
        time.sleep(whole_seconds)

        # 等待小数秒（使用 threading.Timer）
        t = threading.Timer(fractional_seconds, lambda: None)
        t.start()
        t.join()

    # 检测是否连接成功
    def check_connect(self):
        if self.device(resourceId="com.govee.home:id/iv_switch").wait(timeout=10.0):
            return True
        else:
            self.get_log.error('10秒wifi还没连接上，设备详情页加载失败')
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                print("退出详情页")
                # self.logs.info('退出详情页')
            except Exception as e:
                print(e)
            return False


if __name__ == '__main__':
    test = H7151Test()
    n = 1
    while True:
        test.start_test()
