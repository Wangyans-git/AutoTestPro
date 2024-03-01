#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 单个灯具OTA测试
import time
import uiautomator2 as u2
import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Dengju_OTA.get_log import GetLog


class H7161Test:
    def __init__(self):
        self.device = u2.connect_usb('d5cd8968')
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\Dengju_OTA\log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()

    def start_test(self):
        # try:
        self.device(text="Air Quality Monitor").click_exists(timeout=5)
        time.sleep(1)
        if self.check_connect():
            self.device(resourceId='com.govee.home:id/btn_setting').click_exists(timeout=5)
            time.sleep(10)
            for i in range(3):
                self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width, 0.1 * self.height)
            time.sleep(2)
            self.device(resourceId='com.govee.home:id/version_container').click_exists(timeout=5)
            time.sleep(1)
            self.device(resourceId='com.govee.home:id/btn_update').click_exists(timeout=5)
            self.start_update_time = datetime.datetime.now()  # 开始升级时间
            self.check_update_ok()
            self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=5)
            time.sleep(1)
            self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=5)

    # 检测是否连接成功
    def check_connect(self):
        if self.device(resourceId="com.govee.home:id/btn_setting").wait(timeout=10.0):
            return True
        else:
            self.get_log.info('超过10秒设备未连接上，设备详情页加载失败')
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                self.get_log.info('退出详情页')
            except Exception as e:
                print(e)
            return False

    # 检查是否升级成功
    def check_update_ok(self):
        update_success_toast = "升级成功"  # toast弹窗
        update_fail_toast = "蓝牙断开连接，升级失败"  # toast弹窗
        toast = self.device.toast.get_message(180.0, 10.0, 'message').encode('utf-8').decode()
        # print(toast)
        if toast == update_success_toast:
            print("升级成功")
            success_time = datetime.datetime.now()  # 升级成功结束时间
            all_time = success_time - self.start_update_time
            self.get_log.info("升级成功，用时：{}".format(all_time))
        elif toast == update_fail_toast:
            print("蓝牙断开连接，升级失败")
            self.get_log.info("蓝牙断开连接，升级失败")

    # time.sleep(1)
    # device.swipe(0.5 * width, 0.9 * height, 0.5 * width, 0.1 * height)
    # time.sleep(1)
    # device.swipe(0.5 * width, 0.1 * height, 0.5 * width, 0.9 * height)
    # time.sleep(1)
    # time.sleep(1)


if __name__ == '__main__':
    test = H7161Test()
    while True:
        test.start_test()
        time.sleep(5)
