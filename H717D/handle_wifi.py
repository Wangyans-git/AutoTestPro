#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 配网压测
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

import serial
import serial.tools.list_ports
import uiautomator2 as u2

from H717D.logs import get_log


class H7124_Wifi:
    def __init__(self, com, com1, dbs, dbs1, timeout):
        # self.device = u2.connect()
        self.device = u2.connect()
        # self.device = u2.connect('424e4d504c383098')
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        # self.device.settings['operation_delay'] = (1, 1)  # 每次点击后等待2s
        # 脚本日志
        FILE = Path(__file__).resolve()
        ROOT = FILE.parents[1]  # YOLOv5 root directory
        path = str(Path(ROOT) / "H7124/logs/H7124wifi配网压测.txt")
        print(path)
        self.get_log = get_log.GetLog(path)
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H7124'
        self.in_page_num = 0
        try:
            # self.ser = serial.Serial(com,
            #                          dbs,
            #                          timeout=timeout)
            self.relay_ser = serial.Serial(com1,  # 继电器
                                           dbs1,
                                           timeout=timeout)
            print("*********打开串口成功*********")
        except Exception as e:
            print("*********串口异常:{}*********".format(e))
            self.err = -1

    def thread_watch(self):
        thread = threading.Thread(target=self.watch)
        thread.start()

    def watch(self):
        while True:
            # print("复制到粘贴板")
            if self.device(text='知道了').exists():
                self.device(text='知道了').click_exists(timeout=10)

    def add_devise_devices(self):
        # self.thread_watch()   # 处理弹窗
        add_device_num = 0
        add_success_num = 0
        add_fail_num = 0
        while True:
            try:
                """添加设备"""
                # 添加”+“
                if self.device(resourceId="com.govee.home:id/ivDevAdd").exists(timeout=10):
                    self.device(resourceId="com.govee.home:id/ivDevAdd").click_exists(timeout=10)
                    # 输入要添加的SKU
                    self.device(resourceId="com.govee.home:id/tv_search").click_exists(timeout=10)
                    self.device(resourceId="com.govee.home:id/et_search").send_keys(self.sku)
                    # 点击SKU
                    time.sleep(5)
                    while True:
                        self.device(resourceId="com.govee.home:id/sku_des").click_exists(timeout=30)
                        time.sleep(2)
                        self.device(text="继续").click_exists(timeout=10)
                        if self.device(text='H7124_92BA').exists(timeout=10):
                            break
                        else:
                            self.device(text='重新扫描').click_exists(timeout=10)
                    # 选择设备  H5086_681B   H5086_67c9
                    while True:
                        self.device(text='H7124_92BA').click_exists(timeout=10)
                        time.sleep(1)
                        if self.device(text='设备Wi-Fi指示灯以白色快闪，请短按设备电源键').exists(timeout=10):
                            break
                        else:
                            if self.device(text="重新连接").exists(timeout=5):
                                self.device(text="重新连接").click_exists(timeout=5)
                            print("sku点不到了")
                # 命名设备
                print("点击配对")
                if self.device(text='设备Wi-Fi指示灯以白色快闪，请短按设备电源键').exists(timeout=30):
                    time.sleep(2)
                    try:    # 继电器模拟点击配对
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                    except Exception as e:
                        print("继电器串口错误：", e)
                    if self.device(resourceId='com.govee.home:id/done').exists(timeout=10):
                        add_device_num += 1
                        print("配对次数：", add_device_num)
                        self.get_log.info("配对次数：{}".format(add_device_num))
                        self.old_time = datetime.now()
                    else:
                        subprocess.call(['adb', 'shell', 'am', 'force-stop', 'com.govee.home'])
                        time.sleep(2)
                        self.device.app_start('com.govee.home')
                        continue
                if self.device(resourceId='com.govee.home:id/done').exists(timeout=30):
                    self.device(resourceId="com.govee.home:id/sensor_name_edit").click_exists(timeout=10)
                    self.device(resourceId="com.govee.home:id/sensor_name_edit").send_keys(self.sku)
                    self.device(resourceId="com.govee.home:id/done").click_exists(timeout=10)

                # 跳过配网
                # if self.device(resourceId='com.govee.home:id/skip').exists(timeout=10):
                #     while True:
                #         print("跳过")
                #         self.device(resourceId='com.govee.home:id/skip').click_exists(timeout=10)
                #         if self.device(resourceId="com.govee.home:id/btn_done").exists(timeout=10):
                #             self.device(resourceId="com.govee.home:id/btn_done").click_exists(timeout=10)
                #         if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=30):
                #             break
                #         else:
                #             self.error_handle()

                # wifi配置
                # if self.device(text='Govee-2.4g').exists(timeout=10):
                #     self.device(resourceId="com.govee.home:id/et_pwd").clear_text()
                #     self.device(resourceId="com.govee.home:id/et_pwd").send_keys("starstarlight")
                #     while True:
                #         print("配网")
                #         self.device(resourceId="com.govee.home:id/send_wifi").click_exists(timeout=10)
                #         if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=60):
                #             break
                #         else:
                #             self.error_handle()
                if self.device(text='ASUS_F0_2G').exists(timeout=10):
                    self.device(resourceId="com.govee.home:id/et_pwd").clear_text()
                    self.device(resourceId="com.govee.home:id/et_pwd").send_keys("20170201")
                    while True:
                        print("配网")
                        self.device(resourceId="com.govee.home:id/send_wifi").click_exists(timeout=10)
                        if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=60):
                            break
                        else:
                            self.error_handle()

                if self.device(resourceId='com.govee.home:id/iv_switch').exists(timeout=30):
                    add_success_num += 1
                    print("配对配网成功次数：", add_success_num)
                    self.get_log.info("配对配网成功次数：{}".format(add_success_num))
                    new_time = datetime.now()
                    now_time = new_time - self.old_time
                    print("配对时长：", now_time)
                    self.get_log.info("配对时长：{}".format(now_time))
                self.del_device()
            except Exception as e:
                print("绑定出错：",e)
                print("出现异常，重启app")
                subprocess.call(['adb', 'shell', 'am', 'force-stop', 'com.govee.home'])
                time.sleep(2)
                self.device.app_start('com.govee.home')
                if self.device(text=self.sku).exists(timeout=10):
                    self.device(text=self.sku).click_exists(timeout=10)
                    self.del_device()
                else:
                    pass

    def down(self):
        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                          0.1 * self.height)  # 向下滑动

    def up(self):
        time.sleep(2)
        self.device.swipe(0.5 * self.width, 0.1 * self.height, 0.5 * self.width,
                          0.9 * self.height)  # 向下滑动
        time.sleep(2)

    def error_handle(self):
        if self.device(resourceId="com.govee.home:id/iv_switch").wait(timeout=10.0):
            return True
        else:
            self.get_log.error('10秒wifi还没连接上，设备详情页加载失败')
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/ivBack").click_exists(timeout=10.0)
                print("退出详情页")
                self.up()
                self.device(text=self.sku).click_exists(timeout=10.0)
                # self.logs.info('退出详情页')
            except Exception as e:
                print("错误",e)
            return False

    """ 删除设备 """
    def del_device(self):
        # 设置
        if self.device(resourceId="com.govee.home:id/ivRightMost").exists(timeout=10):
            print("删除设备")
            self.device(resourceId="com.govee.home:id/ivRightMost").click_exists(timeout=10)
            time.sleep(2)
            self.down()
            time.sleep(2)
            while True:
                self.down()
                self.device(text="删除设备").click_exists(timeout=10)
                time.sleep(2)
                print("删除")
                if self.device(resourceId="com.govee.home:id/btn_done").exists(timeout=10):
                    time.sleep(2)
                    break
            self.device(resourceId="com.govee.home:id/btn_done").click_exists(timeout=10)

            # if self.device(resourceId="com.govee.home:id/tvComfirm").exists(timeout=10):  # 错误
            #     self.device(resourceId="com.govee.home:id/tvComfirm").click_exists(timeout=10)
            time.sleep(5)


if __name__ == '__main__':
    handle_H7124 = H7124_Wifi('com7', 'com7', 115200, 9600, 1)  # com为串口日志，com1为继电器
    handle_H7124.add_devise_devices()
