#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 单机压测
import threading
import time
import uiautomator2 as u2

from logs.get_log import GetLog


class H7135Test:
    def __init__(self):
        self.device = u2.connect_usb()
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog("H7135_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H7135'

    def start_test(self):

        # 判断当前是否需要进入详情页
        if self.device(text=self.sku).wait(timeout=5.0):
            self.device(text=self.sku).click_exists(timeout=5.0)
            time.sleep(5)
            n = 0
            while True:
                if self.check_connect():
                    try:
                        # self.logs.info('退出详情页')
                        # # 判断设备是否是关机状态，如果是就先开机
                        if self.device(resourceId='com.govee.home:id/iv_delay_off_arrow').exists():
                            flag = self.device(resourceId='com.govee.home:id/iv_delay_off_arrow').info[
                                'enabled']  # 开机状态
                            if not flag:  # 如果设备处于可点击状态
                                self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                        elif self.device(resourceId='com.govee.home:id/com.govee.home:id/tvAutoOff').exists():
                            flag = self.device(resourceId='com.govee.home:id/com.govee.home:id/tvAutoOff').info[
                                'enabled']
                            if not flag:  # 如果设备处于可点击状态
                                self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                        if n % 5 == 1:
                            self.device(resourceId='com.govee.home:id/iv_gear_low_icon').click_exists(timeout=5.0)
                            self.get_log.info("低档")
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            time.sleep(1)
                        elif n % 5 == 2:
                            self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').click_exists(timeout=5.0)
                            self.get_log.info("中档")
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            time.sleep(1)
                        elif n % 5 == 3:
                            self.device(resourceId='com.govee.home:id/iv_gear_high_icon').click_exists(timeout=5.0)
                            self.get_log.info("高档")
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            time.sleep(1)
                        elif n % 5 == 4:
                            self.device(resourceId='com.govee.home:id/iv_fan_icon').click_exists(timeout=5.0)
                            self.get_log.info("风扇档")
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            time.sleep(1)
                        elif n % 5 == 0:
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.get_log.info("自动档")
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            time.sleep(1)
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

    def thread_watch(self):
        thread = threading.Thread(target=self.watch)
        thread.start()

    # 监控弹窗
    def watch(self):
        device = u2.connect()
        while True:
            # print("复制到粘贴板")
            if device(text='知道了').exists():
                device(text='知道了').click_exists(timeout=10)
            if device(text='复制到粘贴板').exists():
                device(text='复制到粘贴板').click_exists(timeout=10)
            time.sleep(5)


if __name__ == '__main__':
    test = H7135Test()
    n = 1
    test.thread_watch()       # 处理弹窗
    test.start_test()
