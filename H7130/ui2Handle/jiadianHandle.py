#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
@Time    : 2022/11/9 15:59
@Author  : jhcheng
@FileName: jiadianHandle.py
@SoftWare: PyCharm
"""
from time import sleep
import time
import threading
from H7130.myConfig import setting
import uiautomator2 as u2
from H7130.log.loger2 import Loger

class JiaDianHandle():

    def __init__(self, phone_name, device_name):
        self.device = u2.connect_usb(phone_name)
        # self.device = u2.connect_wifi('192.168.50.84')
        self.device_name = device_name
        self.screen_x, self.screen_y = self.device.window_size()
        self.package_name = "com.govee.home"
        # 脚本日志
        self.loger = Loger(self.device_name).get_py_logger()
        # 截图路径
        self.image_path = setting.TEST_ERROR_Image
        # 串口日志
        self.comLoger = Loger(self.device_name).get_com_logger()
        # 启动APP
        self.device.app_start(self.package_name, activity="com.govee.home.HomeActivity", stop=True, wait=30)

    def jiadian_mode_switch(self, times):
        threading.Thread(target=self.switch_handle, args=(times,)).start()

    def switch_handle(self, times):
        # 进入设备详情页
        if self.enter_device():
            # 检测连接
            if self.check_connect():
                # 主操作流程
                for i in range(times):
                    try:
                        i = i + 1
                        if i % 5 == 1:
                            self.device(resourceId="com.govee.home:id/low_gear_container").click_exists(timeout=3.0)
                            sleep(3)
                            while True:
                                if self.check_connect() is not True:
                                    self.loger.info('切换低档后连接失败')
                                    print('切换低档后连接失败')
                                    self.enter_device()
                                else:
                                    self.loger.info('切换低档后连接成功')
                                    print('切换低档后连接成功')
                                    break
                        elif i % 5 == 2:
                            self.device(resourceId="com.govee.home:id/mid_gear_container").click_exists(timeout=3.0)

                            sleep(3)
                            while True:
                                if self.check_connect() is not True:
                                    self.loger.info('切换中档后连接失败')
                                    print('切换中档后连接失败')
                                    self.enter_device()
                                else:
                                    self.loger.info('切换中档后连接成功')
                                    print('切换中档后连接成功')
                                    break
                        elif i % 5 == 3:
                            self.device(resourceId="com.govee.home:id/high_gear_container").click_exists(timeout=3.0)
                            sleep(3)
                            while True:
                                if self.check_connect() is not True:
                                    self.loger.info('切换高档后连接失败')
                                    print('切换高档后连接失败')
                                    self.enter_device()
                                else:
                                    self.loger.info('切换高档后连接成功')
                                    print('切换高档后连接成功')
                                    break
                        # elif i % 5 == 4:
                        #     self.device(resourceId="com.govee.home:id/iv_fan_bg").click_exists(timeout=3.0)
                        #     sleep(3)
                        #     while True:
                        #         if self.check_connect() is not True:
                        #             self.loger.info('切换风扇档后连接失败')
                        #             print('切换风扇档后连接失败')
                        #             self.enter_device()
                        #         else:
                        #             self.loger.info('切换风扇档后连接成功')
                        #             print('切换风扇档后连接成功')
                        #             break
                        # elif i % 5 == 0:
                        #     self.device(resourceId="com.govee.home:id/iv_auto_bg").click_exists(timeout=3.0)
                        #     sleep(3)
                        #     while True:
                        #         if self.check_connect() is not True:
                        #             self.loger.info('切换自动档后连接失败')
                        #             print('切换自动档后连接失败')
                        #             self.enter_device()
                        #         else:
                        #             self.loger.info('切换自动档后连接成功')
                        #             print('切换自动档后连接成功')
                        #             break
                    except Exception as e:
                        print(e)
            else:
                while True:
                    # 重新进入
                    self.enter_device()
                    if self.check_connect():
                        break
                    else:
                        # 等5秒再进
                        sleep(5)

    # 进入设备详情页
    def enter_device(self):
        # 等待5秒钟
        sleep(10)
        if self.device(text='设备').click_exists(timeout=60.0):
            if self.device(text=self.device_name).click_exists(timeout=30.0):
                print('进入设备详情页')
                self.loger.info('进入设备详情页')
                return True
            else:
                print('没有找到该设备，无法进入设备详情页')
                self.loger.info('没有找到该设备，无法进入设备详情页')
                return False
        else:
            return False

    # 检测是否连接成功
    def check_connect(self):
        if self.device(resourceId="com.govee.home:id/iv_switch").wait(timeout=10.0):
            return True
        else:
            print('10秒wifi还没连接上，设备详情页加载失败')
            self.loger.info('10秒wifi还没连接上，设备详情页加载失败')
            self.screenshot('蓝牙连接失败')
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                print('退出详情页')
                self.loger.info('退出详情页')
            except Exception as e:
                print(e)
            return False

    # 截图
    def screenshot(self, msg):
        # 截图保存
        now = time.strftime("%Y-%m-%d %H-%M-%S")
        image_name = self.image_path + '/' + msg + " " + now + ".png"
        self.device.screenshot(image_name)
