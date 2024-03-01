#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 绑定配网
import os
import subprocess
import time
from datetime import datetime
import uiautomator2 as u2
import serial
import serial.tools.list_ports
from H5108 import get_log


class H5108:

    def __init__(self):
        self.device = u2.connect_usb()
        self.device.app_start('com.govee.home')
        # self.device.implicitly_wait(30)  # 元素等待时间30s
        with self.device.watch_context() as wc:
            wc.when("复制到粘贴板").click()
        # self.device.settings['operation_delay'] = (1, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = get_log.GetLog("H5108.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H5108'

    def in_page(self):
        in_page_num = 0
        while True:
            try:
                self.device(text=self.sku).click_exists(timeout=30)
                if self.device(resourceId='com.govee.home:id/btn_cancel').exists(timeout=5):
                    self.device(resourceId='com.govee.home:id/btn_cancel').click()
                toast = self.device.toast.get_message(120.0, 10.0, '未刷新成功').encode('utf-8').decode()
                # print(toast)
                if toast == '没有新数据':
                    in_page_num += 1
                    print("没有新数据")
                    self.get_log.info("没有新数据")
                    self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=30)
                    print("返回列表页")
                elif toast == "刷新完成":
                    in_page_num += 1
                    print("刷新完成")
                    self.get_log.info("刷新完成")
                    self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=30)
                    print("返回列表页")
                elif toast == '读取蓝牙数据失败':
                    in_page_num += 1
                    print('读取蓝牙数据失败')
                    self.get_log.info('读取蓝牙数据失败')
                    self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=30)
                    print("返回列表页")
                else:
                    in_page_num += 1
                    print('没有toast提示')
                    self.get_log.info('没有toast提示')
                    self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=30)
                    print("返回列表页")
                print("第[{0}]次".format(in_page_num))
                self.get_log.info("第[{0}]次".format(in_page_num))
                time.sleep(5)
            except Exception as e:
                print(e)

    # 告警
    def alarm(self, temp):
        elements = self.device.xpath('//*[@resource-id="com.android.systemui:id/text"]').all()
        for element in elements:
            text = element.attrib.get('text')
            if "超过设定温度" in text:
                print(text)
            elif "电量低" in text:
                print(text)
            else:
                print("没通知")
                pass
        for i in temp:
            self.device(text=i).click_exists(timeout=30)
            self.device(resourceId='com.govee.home:id/btn_setting').click_exists(timeout=30)
            if self.device(text='温度报警').exists(timeout=120):  # 如果设置页加载完成
                print("加载完成")
                time.sleep(2)
                self.device.swipe(0.896, 0.656, 0.201, 0.662, 0.5)  # 滑动到低温度
                time.sleep(65)  # 等待1min后通知
                self.device.swipe( 0.201, 0.662, 0.896, 0.656,0.5)  # 滑动到高温度
                self.device.swipe(0.3 * self.width, 0 * self.height, 0.7 * self.width, 1 * self.height)  # 向下滑动
                time.sleep(2)
                if self.device(text='+ 2').exists(timeout=5):
                    self.device(text='Govee Home').click_exists(timeout=30)
                else:
                    pass
                elements = self.device.xpath('//*[@resource-id="com.android.systemui:id/text"]').all()
                for element in elements:
                    text = element.attrib.get('text')
                    if "超过设定温度" in text:
                        print(text)
                    elif "电量低" in text:
                        print(text)
                    else:
                        print("没通知")
                        pass
                self.device(resourceId='com.android.systemui:id/dismiss_view').click_exists(timeout=10)  # 清除所有通知



if __name__ == '__main__':
    h5108 = H5108()
    temp_list = ['H5108']
    # h5108.in_page()
    h5108.alarm(temp_list)
