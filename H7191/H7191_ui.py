#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 单机压测
import time
import uiautomator2 as u2

from get_log import GetLog


class H7191Test:
    def __init__(self):
        self.device = u2.connect()
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        # self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog("H7136_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H7191'

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
                        if n % 5 == 0:
                            self.device(resourceId='com.govee.home:id/iv_gear_low_icon').click_exists(timeout=5.0)
                            self.get_log.info("低档")
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            # time.sleep(1)
                        elif n % 5 == 1:
                            self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').click_exists(timeout=5.0)
                            self.get_log.info("中档")
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            # time.sleep(1)
                        elif n % 5 == 2:
                            self.device(resourceId='com.govee.home:id/iv_gear_high_icon').click_exists(timeout=5.0)
                            self.get_log.info("高档")
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            # time.sleep(1)
                        elif n % 5 == 3:
                            self.device(resourceId='com.govee.home:id/iv_fan_icon').click_exists(timeout=5.0)
                            self.get_log.info("风扇档")
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            # time.sleep(1)
                        elif n % 5 == 4:
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
                            self.get_log.info("自动档")
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            n += 1
                            # time.sleep(1)

                    except Exception as e:
                        print(e)
                    else:
                        if self.device(resourceId='com.govee.home:id/btn_cancel').exists():
                            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=2)
                            self.get_log.info("又有弹窗了，哪里来的？")
                        elif self.device(resourceId='com.govee.home:id/dialog_done').exists():
                            self.device(resourceId='com.govee.home:id/dialog_done').click_exists(timeout=2)
                            self.get_log.info("又有弹窗了，哪里来的？")
                        elif self.device(resourceId='com.govee.home:id/btn_done').exists():
                            self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=2)
                            self.get_log.info("又有弹窗了，哪里来的？")
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
    test = H7191Test()
    n = 1
    test.start_test()
