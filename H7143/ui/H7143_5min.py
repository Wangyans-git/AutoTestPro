#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 单机压测5min
import time
import random

import uiautomator2 as u2

from H7142.get_log.get_log import GetLog


class H7143Test:
    def __init__(self):
        self.device = u2.connect_usb("R5CRC1V0GLW")
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog("H7143_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()

        self.sku = 'H7143_30min'

    def start_test(self):
        # 判断当前是否需要进入详情页
        if self.device(text=self.sku).wait(timeout=5.0):
            self.device(text=self.sku).click_exists(timeout=5.0)
            time.sleep(5)
            n = 0
            if self.check_connect():
                while True:
                    try:
                        if self.device(resourceId='com.govee.home:id/ivLeakWaterIconWhat').exists():
                            self.get_log.info("缺水了")
                            break
                        # self.logs.info('退出详情页')
                        if n % 2 == 0:    # 手动挡
                            self.device(resourceId='com.govee.home:id/iv_gear_icon').click_exists(timeout=5.0)
                            self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,0.1 * self.height)  # 向下滑
                            random_num = random.randint(1,4)
                            if random_num == 1:
                                self.device(resourceId='com.govee.home:id/iv_light_rgb_switch_ext1').click_exists(timeout=5.0)
                                self.get_log.info("夜灯")
                            if random_num == 2:
                                self.device(resourceId='com.govee.home:id/iv_lock_switch').click_exists(timeout=5.0)
                                self.get_log.info("童锁")
                            if random_num == 3:
                                self.device(resourceId='com.govee.home:id/iv_light_indicator_switch').click_exists(timeout=5.0)
                                self.get_log.info("显示")
                            self.device(resourceId='com.govee.home:id/ivSwitch').click_exists(timeout=5.0)
                            self.get_log.info("热雾")
                            for i in range(4):
                                self.device(resourceId='com.govee.home:id/iv_lock_remind').click_exists(timeout=5.0)
                                self.device(resourceId='com.govee.home:id/dialog_done').click_exists(timeout=5.0)
                                time.sleep(550)
                            self.device.swipe(0.5 * self.width, 0.1 * self.height, 0.5 * self.width, 0.9 * self.height)
                            n += 1
                            # time.sleep(1800)
                        elif n % 2 == 1:
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                                              0.1 * self.height)  # 向下滑
                            random_num = random.randint(1, 4)
                            if random_num == 1:
                                self.device(resourceId='com.govee.home:id/iv_light_rgb_switch_ext1').click_exists(
                                    timeout=5.0)
                                self.get_log.info("夜灯")
                            if random_num == 2:
                                self.device(resourceId='com.govee.home:id/iv_lock_switch').click_exists(timeout=5.0)
                                self.get_log.info("童锁")
                            if random_num == 3:
                                self.device(resourceId='com.govee.home:id/iv_light_indicator_switch').click_exists(
                                    timeout=5.0)
                                self.get_log.info("显示")
                            self.device(resourceId='com.govee.home:id/ivSwitch').click_exists(timeout=5.0)
                            self.get_log.info("热雾")
                            for i in range(4):
                                self.device(resourceId='com.govee.home:id/iv_lock_remind').click_exists(timeout=5.0)
                                self.device(resourceId='com.govee.home:id/dialog_done').click_exists(timeout=5.0)
                                time.sleep(550)
                            self.device.swipe(0.5 * self.width, 0.1 * self.height, 0.5 * self.width, 0.9 * self.height)
                            n += 1
                            # time.sleep(1800)
                        self.get_log.info("第{}次".format(n))
                    except Exception as e:
                        print(e)
                    else:
                        if self.device(resourceId='com.govee.home:id/btn_cancel').exists():
                            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=2)

                        elif self.device(resourceId='com.govee.home:id/dialog_done').exists():
                            self.device(resourceId='com.govee.home:id/dialog_done').click_exists(timeout=2)

                        elif self.device(resourceId='com.govee.home:id/btn_done').exists():
                            self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=2)
                        else:
                            pass


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
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                print("退出详情页")
                # self.logs.info('退出详情页')
            except Exception as e:
                print(e)
            return False


if __name__ == '__main__':
    test = H7143Test()
    n = 1
    test.start_test()
