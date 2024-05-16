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

from logs import get_log


class DistributionNetworkTest:
    def __init__(self, com, com1, dbs, dbs1, timeout, sku, sku_des):
        self.device = u2.connect("R5CR20H14AV")
        # self.device = u2.connect("R5CR20H14AV")
        # self.device = u2.connect('424e4d504c383098')
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        # self.device.settings['operation_delay'] = (1, 1)  # 每次点击后等待2s
        # 脚本日志
        FILE = Path(__file__).resolve()
        ROOT = FILE.parents[1]  # YOLOv5 root directory
        path = str(Path(ROOT) / f"Handle_Wifi/logs/{sku}wifi配网压测.txt")
        self.serial_path = str(
            Path(ROOT) / f"Handle_Wifi/logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}{sku}串口log.txt")
        print(path)
        self.get_log = get_log.GetLog(path)
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = sku
        self.sku_des = sku_des
        self.in_page_num = 0
        self.network_success_num = 0
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

    def add_devise_devices(self):
        # self.thread_watch()   # 处理弹窗
        # self.thread_wifi_success_or_fail()  # 串口判断配网是否成功
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
                        if self.device(text="继续").exists():
                            self.device(text="继续").click_exists(timeout=10)
                        if self.device(text=self.sku_des).exists(timeout=10):
                            break
                        else:
                            self.device(text='重新扫描').click_exists(timeout=10)
                    # 选择设备  H5086_681B   H5086_67c9
                    while True:
                        self.device(text=self.sku_des).click_exists(timeout=10)
                        time.sleep(1)
                        if self.device(text='配对').exists(timeout=10):
                            break
                        else:
                            if self.device(text="重新连接").exists(timeout=5):
                                self.device(text="重新连接").click_exists(timeout=5)
                            if self.device(resourceId='com.govee.home:id/done').exists(timeout=5):
                                break
                            print("sku点不到了")
                # 命名设备
                print("点击配对")

                # 继电器模拟点击配对
                if self.device(text='配对').exists(timeout=30):
                    time.sleep(2)
                    # try:
                    #     self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                    #     time.sleep(0.5)
                    #     self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                    # except Exception as e:
                    #     print("继电器串口错误：", e)

                if self.device(resourceId='com.govee.home:id/done').exists(timeout=30):
                    add_device_num += 1
                    print("配对次数：", add_device_num)
                    self.get_log.info("配对次数：{}".format(add_device_num))
                    self.old_time = datetime.now()
                else:
                    print("配对时出错")
                    self.error_handle()
                if self.device(resourceId='com.govee.home:id/done').exists(timeout=30):
                    while True:
                        self.device(resourceId="com.govee.home:id/sensor_name_edit").click_exists(timeout=10)
                        self.device(resourceId="com.govee.home:id/sensor_name_edit").send_keys(self.sku)
                        self.device(resourceId="com.govee.home:id/done").click_exists(timeout=10)
                        if self.device(text='保存密码').exists(timeout=10):
                            break
                # wifi配置
                if self.device(text='ASUS_F0_2G').exists(timeout=5):
                    self.device(resourceId="com.govee.home:id/et_pwd").clear_text()
                    self.device(resourceId="com.govee.home:id/et_pwd").send_keys("govee123")
                    while True:
                        print("配网")
                        self.device(resourceId="com.govee.home:id/send_wifi").click_exists(timeout=10)
                        if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=60):
                            break
                        else:
                            print("配网时出错")
                            self.error_handle()
                else:
                    # 跳过配网
                    while True:
                        print("跳过")
                        if self.device(resourceId='com.govee.home:id/skip').exists(timeout=10):
                            self.device(resourceId='com.govee.home:id/skip').click_exists(timeout=10)
                            if self.device(resourceId="com.govee.home:id/btn_done").exists(timeout=10):
                                self.device(resourceId="com.govee.home:id/btn_done").click_exists(timeout=10)
                            if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=30):
                                break
                            else:
                                print("跳过时出错")
                                self.error_handle()
                        else:
                            break

                # 绑定完成
                if self.device(resourceId='com.govee.home:id/iv_switch').exists(timeout=30):
                    add_success_num += 1
                    print("配对配网后进入详情页成功次数：", add_success_num)
                    self.get_log.info("配对配网后进入详情页成功次数：{}".format(add_success_num))
                    new_time = datetime.now()
                    now_time = new_time - self.old_time
                    print("配对时长：", now_time)
                    self.get_log.info("配对时长：{}".format(now_time))
                self.del_device()
            except Exception as e:
                print("绑定出错：", e)
                subprocess.call(['adb', 'shell', 'am', 'force-stop', 'com.govee.home'])
                time.sleep(2)
                self.device.app_start('com.govee.home')
                if self.device(text=self.sku).exists(timeout=15):
                    self.device(text=self.sku).click_exists(timeout=10)
                    self.del_device()

    def down(self):
        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                          0.1 * self.height)  # 向下滑动

    def up(self):
        time.sleep(2)
        self.device.swipe(0.5 * self.width, 0.1 * self.height, 0.5 * self.width,
                          0.9 * self.height)  # 向下滑动
        time.sleep(2)

    def error_handle(self):
        while True:
            self.get_log.error("出现异常，重启app")
            print("出现异常，重启app")
            subprocess.call(['adb', 'shell', 'am', 'force-stop', 'com.govee.home'])
            time.sleep(2)
            self.device.app_start('com.govee.home')
            if self.device(text=self.sku).exists(timeout=20):
                self.device(text=self.sku).click_exists(timeout=10)
                if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=30):
                    break
            else:
                self.get_log.info("没添加成功")
                break

    """ 删除设备 """

    def del_device(self):
        # 设置
        if self.device(resourceId="com.govee.home:id/ivRightMost").exists(timeout=5):
            print("删除设备")
            self.device(resourceId="com.govee.home:id/ivRightMost").click_exists(timeout=10)
        elif self.device(resourceId="com.govee.home:id/btn_setting").exists(timeout=5):
            print("删除设备")
            self.device(resourceId="com.govee.home:id/btn_setting").click_exists(timeout=10)
        time.sleep(2)
        self.down()
        time.sleep(2)
        while True:
            self.down()
            if self.device(text="删除设备").exists(timeout=10):
                self.device(text="删除设备").click_exists(timeout=10)
            print("删除")
            if self.device(text="是").exists(timeout=10):
                self.device(text="是").click_exists(timeout=10)
                if self.device(resourceId="com.govee.home:id/ivDevAdd").exists(timeout=10):
                    break
            if self.device(text=self.sku).exists(timeout=5):
                self.device(text=self.sku).click_exists(timeout=5)
                self.del_device()
                break
            else:
                break

    def thread_watch(self):
        thread = threading.Thread(target=self.watch)
        thread.start()

    def thread_wifi_success_or_fail(self):
        thread = threading.Thread(target=self.wifi_success_or_fail)
        thread.start()

    # 处理弹窗
    def watch(self):
        while True:
            # print("复制到粘贴板")
            if self.device(text='知道了').exists():
                self.device(text='知道了').click_exists(timeout=10)
            if self.device(text='复制到粘贴板').exists():
                self.device(text='复制到粘贴板').click_exists(timeout=10)

    # 串口判断是否配网成功
    def wifi_success_or_fail(self):
        date_all = ""
        while True:
            try:
                date_line = self.ser.readline().decode()
                # print(date_line)
                date_all += date_line
                self.write_txt(date_all)
                if "Cloud Device Construct Success" in date_line:
                    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.network_success_num += 1
                    self.get_log.info("{0}配网成功{1}次".format(now_time, self.network_success_num))
            except Exception as e:
                print(e)

    # 记录串口文件
    def write_txt(self, log):
        result = str(log)
        try:
            with open(self.serial_path, 'w') as file_handle:
                file_handle.write(result)
        except Exception as e:
            print("文件读写出错：", e)


if __name__ == '__main__':
    sku_ = "H7148"
    sku_des_ = "H7148_E4B2"
    handle_wifi = DistributionNetworkTest('com3', 'com4', 115200, 9600, 1, sku_, sku_des_)  # com为串口日志，com1为继电器
    handle_wifi.add_devise_devices()
