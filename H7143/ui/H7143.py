#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 随机按键
import time
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
        self.sku = 'H7143_5min'

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
                        if n % 2 == 1:   # 手动挡
                            # self.device(resourceId='com.govee.home:id/iv_gear_low_icon').click_exists(timeout=5.0)
                            # self.get_log.info("低档")
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/ivSwitch').click_exists(timeout=5.0)
                            # self.get_log.info("冷雾")
                            print("冷雾")
                            n += 1
                            time.sleep(30)
                        elif n % 2 == 0:
                            # self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').click_exists(timeout=5.0)
                            # self.get_log.info("中档")
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.device(resourceId='com.govee.home:id/ivSwitch').click_exists(timeout=5.0)
                            # self.get_log.info("热雾")
                            print("热雾")
                            n += 1
                            time.sleep(30)


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
    while True:
        test.start_test()
