#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 单机压测
import time
import uiautomator2 as u2

from H7142.get_log.get_log import GetLog


class H7151Test:
    def __init__(self):
        self.device = u2.connect_usb('d5cd8968')
        # self.device = u2.connect_usb('424e4d504c383098')
        self.device.app_start('com.govee.home')
        # self.device.implicitly_wait(30)  # 元素等待时间30s
        self.device.settings['wait_timeout'] = 10  # 元素等待时间30s
        self.device.settings['operation_delay'] = 1  # 每次点击后等待1s
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\H7135_Auto\get_log\H7135_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H7151-3'

    def start_test(self):
        # 判断当前是否需要进入详情页
        if self.device(text=self.sku).wait(timeout=5.0):
            self.device(text=self.sku).click_exists(timeout=5.0)
            time.sleep(5)
            print("循环")
            n = 0
            if self.check_connect():
                while True:
                    try:
                        # self.logs.info('退出详情页')
                        if n % 4 == 0:
                            self.device(resourceId='com.govee.home:id/iv_gear_low_icon').click_exists(timeout=5.0)
                            self.get_log.info("低档")
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.gear()
                            n += 1
                        elif n % 4 == 1:
                            self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').click_exists(timeout=5.0)
                            self.get_log.info("中档")
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.gear()
                            n += 1
                        elif n % 4 == 2:
                            self.device(resourceId='com.govee.home:id/iv_gear_high_icon').click_exists(timeout=5.0)
                            self.get_log.info("高档")
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.gear()
                            n += 1
                        elif n % 4 == 3:
                            self.device(resourceId='com.govee.home:id/iv_dry_clothes_icon').click_exists(timeout=5.0)
                            self.get_log.info("干衣档")
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.gear()
                            n += 1
                    except Exception as e:
                        print(e)
                    print(self.sku,"已经测试了{}次".format(n))
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
        self.device.click(0.177, 0.861)  # 1档
        self.pop()
        self.device.click(0.316, 0.861)  # 2档
        self.pop()
        self.device.click(0.481, 0.861)  # 3档
        self.pop()
        self.device.click(0.618, 0.861)  # 4档
        self.pop()
        self.device.click(0.765, 0.861)  # 5档
        self.pop()
        self.device.click(0.177, 0.861)  # 1档
        self.pop()
        self.device.click(0.316, 0.861)  # 2档
        self.pop()
        self.device.click(0.481, 0.861)  # 3档
        self.pop()
        self.device.click(0.618, 0.861)  # 4档
        self.pop()
        self.device.click(0.765, 0.861)  # 5档
        self.pop()

    def pop(self):
        if self.device(resourceId='com.govee.home:id/btn_done').exists():
            self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=5.0)

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
