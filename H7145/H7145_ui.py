#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 客诉问题压测
import time
import uiautomator2 as u2

from H7145.logs.get_log import GetLog


class H7145Test:
    def __init__(self):
        # self.device = u2.connect_usb('d5cd8968')
        self.device = u2.connect_usb()
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog("logs/H7145_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H7143'
        self.n = 0  # 循环计数
        self.m = 0  # 间隔计数
        self.flag = 0  # 单数切档位 双数不切

    def start_test(self):
        # 判断当前是否需要进入详情页
        if self.device(text=self.sku).wait(timeout=5.0):
            self.device(text=self.sku).click_exists(timeout=5.0)
            time.sleep(5)
            self.device(resourceId='com.govee.home:id/iv_gear_icon').click_exists(timeout=10.0)
            while True:
                if self.check_connect():
                    try:
                        while True:
                            self.one()
                            if self.flag % 2 == 1:
                                break
                        while True:
                            self.two()
                            if self.flag % 2 == 0:
                                break
                    except Exception as e:
                        print(e)
                else:
                    while True:
                        self.device(text=self.sku).click_exists(timeout=5.0)
                        if self.check_connect():
                            break
                        else:
                            time.sleep(5)
        else:
            print("没有改找到该设备名的设备!")

    def one_wait_num(self, num):
        print("1----", num)
        if num % 4 == 0:

            self.get_log.info("1等待5s")
            print("1等待5s")
            print("=============")
            time.sleep(5)
        elif num % 4 == 1:

            self.get_log.info("1等待10s")
            print("1等待10s")
            print("=============")
            time.sleep(10)
        elif num % 4 == 2:

            self.get_log.info("1等待15s")
            print("1等待15s")
            print("=============")
            time.sleep(15)
        elif num % 4 == 3:
            self.get_log.info("1等待10min")
            print("1等待10min")
            print("=============")
            time.sleep(600)

    def two_wait_num(self, num):
        print("2----",num)
        if num % 3 == 0:
            # self.m += 1
            self.get_log.info("1等待5s")
            print("2等待5s")
            print("=============")
            time.sleep(5)
        elif num % 3 == 1:
            # self.m += 1
            self.get_log.info("1等待10s")
            print("2等待10s")
            print("=============")
            time.sleep(10)
        elif num % 3 == 2:
            self.get_log.info("1等待10min")
            print("2等待10min")
            print("=============")
            # self.m = 0
            time.sleep(600)

    def one(self):
        if self.n % 4 == 0:
            self.device.click(0.337, 0.797)  # 3档
            self.get_log.info("1三档")
            print("1三档")
            self.n += 1
            self.one_wait_num(self.m)
        elif self.n % 4 == 1:
            self.device.click(0.154, 0.792)  # 1档
            self.get_log.info("1一档")
            print("1一档")
            self.n += 1
            self.one_wait_num(self.m)
        elif self.n % 4 == 2:
            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
            self.get_log.info("1自动档")
            print("1自动档")
            self.n += 1
            self.one_wait_num(self.m)
        elif self.n % 4 == 3:
            self.device(resourceId='com.govee.home:id/iv_gear_icon').click_exists(timeout=5.0)
            self.get_log.info("1手动档")
            print("1手动档")
            self.n = 0
            self.one_wait_num(self.m)
            self.flag += 1

    def two(self):
        if self.n % 3 == 0:
            self.device.click(0.337, 0.797)  # 3档
            self.get_log.info("2三档")
            print("2三档")
            self.n += 1
            self.two_wait_num(self.m)
        elif self.n % 3 == 1:
            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
            self.get_log.info("2自动档")
            print("2自动档")
            self.n += 1
            self.two_wait_num(self.m)
        elif self.n % 3 == 2:
            self.device(resourceId='com.govee.home:id/iv_gear_icon').click_exists(timeout=5.0)
            self.get_log.info("2手动档")
            print("2手动档")
            self.n = 0
            self.two_wait_num(self.m)
            self.flag += 1
            self.m += 1  #

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
    test = H7145Test()
    n = 1
    while True:
        test.start_test()
