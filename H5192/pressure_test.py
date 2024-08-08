#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 压力测试
import subprocess
import time

import uiautomator2 as u2

from H5192.logs import get_log


class H5192:

    def __init__(self):
        self.device = u2.connect()
        self.device.implicitly_wait(30)  # 元素等待时间30s
        # self.device.settings['operation_delay'] = (1, 1)  # 每次点击后等待2s
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        # 脚本日志
        self.get_log = get_log.GetLog("logs/H5192.txt")
        self.sku = 'H5192'
        self.refresh_data_num = 0

    # 数据拉取压测
    def refresh_data(self):
        while True:
            try:
                self.Log_in()
                self.device(text=self.sku).click_exists(timeout=5)
                if self.device(resourceId='com.govee.home:id/iv_to_chart_page_4_h5199_detail').exists(timeout=15):
                    time.sleep(10)
                    while True:
                        self.device(resourceId='com.govee.home:id/iv_to_chart_page_4_h5199_detail').click_exists(timeout=5)
                        if self.device(text="环境温度").exists(timeout=5.0):
                            self.refresh_data_num += 1
                            self.get_log.info(f"刷新第{self.refresh_data_num}次")
                            print(f"刷新第{self.refresh_data_num}次")
                            time.sleep(60)
                            break
                else:
                    while True:
                        self.device(text=self.sku).click_exists(timeout=5.0)
                        if self.enter_device(self.sku):
                            break
                        else:
                            time.sleep(5)

            except Exception as e:
                print("错误",e)
                pass

    # 进入详情页验证
    def enter_device(self, sku=None):
        if self.device(resourceId="com.govee.home:id/iv_to_chart_page_4_h5199_detail").exists(timeout=30):
            print("进入详情页")
            self.get_log.info("进入{0}详情页成功".format(sku))
            return True
        else:
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/iv_go_back_4_h5199_tc").click_exists(timeout=5.0)
                print("{0}30秒还未进入详情页，连接设备失败，退出详情页".format(sku))
                self.get_log.info("{0}30秒还未进入详情页，连接设备失败，退出详情页".format(sku))
            except Exception as e:
                print(e)
            return False

    def Log_in(self):
        subprocess.run(['adb', 'shell', 'pm', 'clear', 'com.govee.home'])
        self.device.app_start('com.govee.home')
        time.sleep(5)
        self.light()  # 左滑动
        self.device(text="允许").click(timeout=5)
        self.device(text="同意并使用").click(timeout=5)
        self.device(resourceId="com.govee.home:id/ivTabProfile").click(timeout=5)
        while not self.device(text="邮箱").exists():
            print("登录")
            self.device(text="登录").click(timeout=5)
        self.device(text="邮箱").click(timeout=5)
        self.device(text="邮箱").send_keys("951772384@qq.com")
        self.device(text="密码").click(timeout=5)
        self.device(text="密码").send_keys("govee123")
        self.device(text="登录").click(timeout=5)
        self.device(resourceId="com.govee.home:id/ivTabDevice").click(timeout=5)
        self.device(text="允许").click(timeout=5)
        self.device(text="仅在使用该应用时允许").click(timeout=5)
        self.device(text="取消").click(timeout=5)
        self.device(text="知道了").click(timeout=5)

    def down(self):
        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                          0.1 * self.height)  # 向下滑动

    def up(self):
        self.device.swipe(0.5 * self.width, 0.1 * self.height, 0.5 * self.width,
                          0.9 * self.height)  # 向上滑动

    def light(self):
        for i in range(4):
            # self.device.swipe(0.9 * self.width, 0.5 * self.height, 0.1 * self.width,
            #                   0.5 * self.height)  # 向上滑动
            self.device.click(0.548, 0.459)
            time.sleep(1)


if __name__ == '__main__':
    handle_H5086 = H5192()
    handle_H5086.refresh_data()
