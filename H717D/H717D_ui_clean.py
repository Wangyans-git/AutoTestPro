#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 两台设备清洁压测
import threading
import time

import uiautomator2 as u2

from H717D.logs.get_log import GetLog


class H717DTest:
    def __init__(self):
        self.device = u2.connect("424e4d504c383098")
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        # self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog("H717D_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()

    def start_test(self, sku_list):
        self.thread_handle_pop()
        # 判断当前是否需要进入详情页
        while True:
            for sku in sku_list:
                print(sku)
                if self.device(text=sku).exists(timeout=5.0):
                    self.device(text=sku).click_exists(timeout=5.0)
                    time.sleep(5)
                    # self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width, 0.1 * self.height)
                    if self.check_connect():
                        try:
                            self.device(text='执行').click_exists(timeout=10)
                            self.get_log.info("清洁")
                            time.sleep(2)
                        except Exception as e:
                            print(e)
                    else:
                        while True:
                            self.device(text=sku).click_exists(timeout=5.0)
                            if self.check_connect():
                                break
                            else:
                                time.sleep(5)
                    self.device(resourceId="com.govee.home:id/ivBack").click_exists(timeout=5.0)
                else:
                    print("没有改找到该设备名的设备!")
                time.sleep(3)
            n = 0
            while True:
                self.device(text='设备').click_exists(timeout=10)
                if n == 66:
                    print("关机")
                    break
                n += 1
                print(n)
                time.sleep(10)  # 73

    def handle_pop(self):
        while True:
            if self.device(resourceId='com.govee.home:id/btn_done').exists():
                self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=5)
            if self.device(resourceId='com.govee.home:id/done').exists():
                self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=5)
            if self.device(text="已清理污水").exists():
                self.device(text="已清理污水").click_exists(timeout=5)
            time.sleep(3)

    def thread_handle_pop(self):
        thread = threading.Thread(target=self.handle_pop)
        thread.start()

    # 检测是否连接成功
    def check_connect(self):
        if self.device(resourceId="com.govee.home:id/iv_switch").wait(timeout=10.0):
            return True
        else:
            self.get_log.error('10秒wifi还没连接上，设备详情页加载失败')
            # 退出详情页
            try:
                if self.device(resourceId="com.govee.home:id/btn_back").exists():
                    self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                elif self.device(resourceId="com.govee.home:id/ivBack").exists():
                    self.device(resourceId="com.govee.home:id/ivBack").click_exists(timeout=5.0)
                print("退出详情页")
                # self.logs.info('退出详情页')
            except Exception as e:
                print(e)
            return False


if __name__ == '__main__':
    test_list = ['H717D', 'H717D1']
    test = H717DTest()
    test.start_test(test_list)
