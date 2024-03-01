#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 作用
import subprocess
import threading
import time
import uiautomator2 as u2
import serial
import serial.tools.list_ports

from H5086.logs import get_log
from pathlib import Path
from datetime import datetime

class H7135_Wifi:
    def __init__(self, com, com1, dbs, dbs1, timeout):
        # self.device = u2.connect_usb()
        self.device = u2.connect_usb('d5cd8968')
        # self.device = u2.connect_usb('424e4d504c383098')
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        # self.device.settings['operation_delay'] = (1, 1)  # 每次点击后等待2s
        # 脚本日志
        FILE = Path(__file__).resolve()
        ROOT = FILE.parents[1]  # YOLOv5 root directory
        path = str(Path(ROOT) / "logs/H7135wifi配网压测.log")
        self.get_log = get_log.GetLog(path)
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H7135'
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
            with self.device.watch_context() as wc:
                wc.when("复制到粘贴板").click()

    def add_devise_devices(self):
        add_device_num = 0
        add_success_num = 0
        add_fail_num = 0
        while True:
            try:
                """添加设备"""
                # 添加”+“
                if self.device(resourceId="com.govee.home:id/ivDevAdd").exists(timeout=60):
                    self.device(resourceId="com.govee.home:id/ivDevAdd").click_exists(timeout=30)
                    # 输入要添加的SKU
                    self.device(resourceId="com.govee.home:id/tv_search").click_exists(timeout=30)
                    self.device(resourceId="com.govee.home:id/et_search").send_keys(self.sku)
                    # 点击SKU
                    time.sleep(5)
                    while True:
                        self.device(resourceId="com.govee.home:id/sku_des").click_exists(timeout=60)
                        time.sleep(2)
                        if self.device(text='H7135_905B').exists(timeout=30):
                            break
                    # 选择设备  H5086_681B   H5086_67c9
                    while True:
                        self.device(text='H7135_905B').click_exists(timeout=60)
                        print("sku点不到了")
                        time.sleep(1)
                        if self.device(text='设备Wi-Fi指示灯以白色慢闪，请短按设备电源键').exists(timeout=30):
                            break
                # 命名设备
                print("点击配对")
                if self.device(text='设备Wi-Fi指示灯以白色慢闪，请短按设备电源键').exists(timeout=60):
                    time.sleep(2)
                    try:
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                    except Exception as e:
                        print("继电器串口错误：", e)
                    if self.device(resourceId='com.govee.home:id/done').exists(timeout=60):
                        add_device_num += 1
                        print("配对次数：", add_device_num)
                        self.get_log.info("配对次数：{}".format(add_device_num))
                        self.old_time = datetime.now()
                    else:
                        subprocess.call(['adb', 'shell', 'am', 'force-stop', 'com.govee.home'])
                        time.sleep(2)
                        self.device.app_start('com.govee.home')
                        continue
                if self.device(resourceId='com.govee.home:id/done').exists(timeout=60):
                    self.device(resourceId="com.govee.home:id/sensor_name_edit").click_exists(timeout=30)
                    self.device(resourceId="com.govee.home:id/sensor_name_edit").send_keys(self.sku)
                    self.device(resourceId="com.govee.home:id/done").click_exists(timeout=30)
                # wifi配置
                if self.device(text='Govee-2.4g').exists(timeout=60):
                    self.device(resourceId="com.govee.home:id/et_pwd").clear_text()
                    
                    self.device(resourceId="com.govee.home:id/et_pwd").send_keys("starstarlight")
                    
                    while True:
                        print("配网")
                        self.device(resourceId="com.govee.home:id/send_wifi").click_exists(timeout=30)
                        
                        if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=60):
                            break
                elif self.device(text='Aircove-AX1800').exists(timeout=60):
                    self.device(resourceId="com.govee.home:id/et_pwd").clear_text()
                    self.device(resourceId="com.govee.home:id/et_pwd").send_keys("20170201")
                    while True:
                        print("配网")
                        self.device(resourceId="com.govee.home:id/send_wifi").click_exists(timeout=30)
                        if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=60):
                            break
                else:
                    self.device(resourceId='com.govee.home:id/skip').click_exists(timeout=30)
                    self.device(text='确认').click_exists(timeout=30)
                    self.get_log.info("未配网")
                    pass
                if self.device(resourceId='com.govee.home:id/iv_switch').exists(timeout=180):
                    add_success_num += 1
                    print("配对配网成功次数：", add_success_num)
                    self.get_log.info("配对配网成功次数：{}".format(add_success_num))
                    new_time = datetime.now()
                    now_time = new_time - self.old_time
                    print("配对时长：", now_time)
                    self.get_log.info("配对时长：{}".format(now_time))
                    if add_device_num == 500:
                        print("测试完成")
                        break
                else:
                    print("没有配网成功")
                    self.get_log.info("没有配网成功")
                # 设置
                if self.device(resourceId="com.govee.home:id/btn_setting").exists(timeout=30):
                    print("删除设备")
                    self.device(resourceId="com.govee.home:id/btn_setting").click_exists(timeout=30)
                    
                    """ 删除设备 """
                    time.sleep(2)
                    self.down()
                    time.sleep(2)
                    while True:
                        self.down()
                        self.device(resourceId="com.govee.home:id/btn_delete").click_exists(timeout=30)
                        
                        time.sleep(2)
                        # if self.device(resourceId="com.govee.home:id/tvComfirm").exists(timeout=5):  # 错误
                        #     self.device(resourceId="com.govee.home:id/tvComfirm").click_exists(timeout=30)
                        print("删除")
                        if self.device(resourceId="com.govee.home:id/btn_done").exists(timeout=30):
                            time.sleep(2)
                            break
                    self.device(resourceId="com.govee.home:id/btn_done").click_exists(timeout=30)
                    
                    # if self.device(resourceId="com.govee.home:id/tvComfirm").exists(timeout=5):  # 错误
                    #     self.device(resourceId="com.govee.home:id/tvComfirm").click_exists(timeout=30)
                    time.sleep(5)
            except Exception as e:
                print(e)

    def handle_pop(self):
        pass
        # while True:
        #     if self.device(text='复制到粘贴板').exists(timeout=2):
        #         self.device(text='复制到粘贴板').click_exists(timeout=60)
        #     else:
        #         break

    def down(self):
        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                          0.1 * self.height)  # 向下滑动


if __name__ == '__main__':
    handle_H7135 = H7135_Wifi('com7', 'com7', 115200, 9600, 1)  # com为串口日志，com1为继电器
    # test_list = ['Smart Plug Pro4']
    # handle_H7135.thread_watch()
    handle_H7135.add_devise_devices()
