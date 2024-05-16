#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 单机压测
import threading
import time

import uiautomator2 as u2

from H717D.logs.get_log import GetLog


class H717DTest:
    def __init__(self, sku_list):
        self.device = u2.connect("424e4d504c383098")
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog("H717D_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku_list = sku_list

    def start_test(self):
        # 判断当前是否需要进入详情页
        for sku in self.sku_list:
            if self.device(text=sku).wait(timeout=5.0):
                self.device(text=sku).click_exists(timeout=5.0)
                time.sleep(5)
                n = 0
                self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width, 0.1 * self.height)
                while True:
                    if self.check_connect():
                        try:
                            self.logs.info('退出详情页')
                            if n % 7 == 0:
                                self.device(resourceId='com.govee.home:id/ivMode1icon').click_exists(timeout=10)
                                self.device(text="确认").click_exists(timeout=10)
                                while self.device(text='确定要取消制冰？').exists():
                                    self.device(text="确认").click_exists(timeout=10)
                                self.get_log.info("小冰")
                                n += 1
                                time.sleep(2)
                            elif n % 7 == 1:
                                self.device(resourceId='com.govee.home:id/ivMode2icon').click_exists(timeout=10)
                                self.device(text="确认").click_exists(timeout=10)
                                while self.device(text='确定要取消制冰？').exists():
                                    self.device(text="确认").click_exists(timeout=10)
                                self.get_log.info("中冰")
                                n += 1
                                time.sleep(2)
                            elif n % 7 == 2:
                                self.device(resourceId='com.govee.home:id/ivMode3icon').click_exists(timeout=10)
                                self.device(text="确认").click_exists(timeout=10)
                                while self.device(text='确定要取消制冰？').exists():
                                    self.device(text="确认").click_exists(timeout=10)
                                self.get_log.info("大冰")
                                n += 1
                                time.sleep(2)
                            elif n % 7 == 3:
                                self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=10)
                                self.device(text="确认").click_exists(timeout=10)
                                while self.device(text='确定要取消制冰？').exists():
                                    self.device(text="确认").click_exists(timeout=10)
                                self.get_log.info("关机")
                                n += 1
                                time.sleep(2)
                            elif n % 7 == 4:
                                self.device(text='执行').click_exists(timeout=10)
                                self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=10)
                                while True:
                                    self.device(resourceId='com.govee.home:id/done').click_exists(timeout=10)
                                    if self.device(resourceId='com.govee.home:id/ivMode2icon').exists():
                                        break
                                self.get_log.info("清洁")
                                n += 1
                                time.sleep(2)

                            elif n % 7 == 5:
                                self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=10)
                                self.get_log.info("开机")
                                n += 1
                                time.sleep(2)
                            elif n % 7 == 6:
                                for i in range(2):
                                    self.device.xpath(
                                        '//*[@resource-id="com.govee.home:id/cl_light"]/android.widget.ImageView[2]').click_exists(
                                        timeout=5.0)
                                self.get_log.info("夜灯开关")
                                n += 1
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
            else:
                print("没有改找到该设备名的设备!")

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
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                print("退出详情页")
                # self.logs.info('退出详情页')
            except Exception as e:
                print(e)
            return False


if __name__ == '__main__':
    test_list = ['H717D', 'H717D1']
    test = H717DTest(test_list)
    test.start_test()
