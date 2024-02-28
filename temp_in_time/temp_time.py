#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 5105进入相情也时间压测
import datetime
import time
import uiautomator2 as u2
import subprocess
from PIL import Image, ImageChops, ImageGrab
import os
import cv2
from openpyxl.workbook import Workbook

from H7142.get_log.get_log import GetLog


class H5105Test:
    def __init__(self):
        self.device = u2.connect_usb('d5cd8968')
        # self.device = u2.connect_usb('R5CW221RRGB')
        # self.device = u2.connect_usb('424e4d504c383098')
        # self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        # self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog(r"C:\wys\AutoTestProjects\temp_in_time\logs\H5105_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H5105'
        self.test_num = 0
        # self.test_date = []
        # 创建一个新的工作簿
        self.workbook = Workbook()
        # 获取默认的活动工作表
        self.sheet = self.workbook.active
        self.sheet.append(['测试次数', '刷新成功时间'])

    # 杀后台
    def start_test_kill(self):
        try:
            self.device.app_start('com.govee.home')
            time.sleep(5)  # 等待5分钟
            if self.device(text=self.sku).exists():
                self.device(text=self.sku).click_exists(timeout=60)
                start_time = datetime.datetime.now()
                print("点击时间为：{}".format(start_time))
            if self.device(resourceId='com.govee.home:id/btn_setting').exists(timeout=30):
                self.device(resourceId='com.govee.home:id/btn_setting').click_exists(timeout=5)
                print("进入详情页")
                self.test_num += 1
                if self.device(resourceId='com.govee.home:id/setting_tempture_alarm').click_exists(timeout=1):
                    end_time = datetime.datetime.now()
                    in_time = end_time - start_time
                    total_seconds = in_time.total_seconds()  # 转换成秒
                    hours = int(total_seconds // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    formatted_time_diff = f"{hours}小时{minutes}分钟{seconds}秒"
                    print("刷新成功时间为：{}".format(end_time))
                    print("刷新成功时间为：{}".format(formatted_time_diff))
                    print(f"测试了{self.test_num}次")
                    self.get_log.info(f"测试了{self.test_num}次")
                    self.get_log.info("刷新成功时间为：{}".format(formatted_time_diff))
                    self.sheet.append([f"第{self.test_num}次", formatted_time_diff])  # 插入数据到excel表格中
                else:
                    self.get_log.error("2分钟仍未连接成功")
                    self.sheet.append([f"第{self.test_num}次", "2分钟仍未连接成功"])
                self.workbook.save(filename="../temp_in_time/excel/example.xlsx")
                subprocess.call(['adb', 'shell', 'am', 'force-stop', 'com.govee.home'])
                if self.test_num % 500 == 0:
                    print("手机重启蓝牙模块")
                    os.system('adb reboot')
                    time.sleep(80)
                    os.system('adb shell input keyevent 26')
                    time.sleep(10)
                    print("点击第一次")
                    self.device.xpath(
                        '//*[@resource-id="com.android.systemui:id/notification_stack_scroller"]/android.widget.FrameLayout[1]').long_click()
            time.sleep(3)

            # time.sleep(5)
        except Exception:
            pass


if __name__ == '__main__':
    test = H5105Test()
    while True:
        # test.handel_Date()
        test.start_test_kill()
