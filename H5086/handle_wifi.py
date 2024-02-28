#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : H5086压测
import subprocess
import time
from datetime import datetime
import uiautomator2 as u2
import serial
import serial.tools.list_ports
from H5086.logs import get_log


class H5086:

    def __init__(self, com, com1, dbs, dbs1, timeout):
        # self.device = u2.connect_usb('R5CW221RRGB')
        # self.device = u2.connect_usb('424e4d504c383098')
        # self.device = u2.connect_usb()
        # self.device.app_start('com.govee.home')
        # self.device.implicitly_wait(30)  # 元素等待时间30s
        # self.device.settings['operation_delay'] = (1, 1)  # 每次点击后等待2s
        # 获取手机分辨率
        # self.width, self.height = self.device.window_size()
        # with self.device.watch_context() as wc:
        #     wc.when().click()    # 出现弹窗就点击
        # 脚本日志
        self.get_log = get_log.GetLog("logs/H5086.log")
        self.sku = 'H5086'
        self.in_page_num = 0
        # self.device.unlock()  # 解锁屏幕
        try:
            self.ser = serial.Serial(com,
                                     dbs,
                                     timeout=timeout)
            self.relay_ser = serial.Serial(com1,  # 继电器
                                           dbs1,
                                           timeout=timeout)
            print("*********打开串口成功*********")
        except Exception as e:
            print("*********串口异常:{}*********".format(e))
            self.err = -1

    # 配网压测
    def add_devise_devices(self):
        add_device_num = 0
        add_success_num = 0
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
                        if self.device(text='H5086_681B').exists(timeout=30):
                            break
                    # 选择设备  H5086_681B   H5086_67c9
                    while True:
                        self.device(text='H5086_681B').click_exists(timeout=60)
                        print("sku点不到了")
                        time.sleep(1)
                        if self.device(text='设备此时蓝灯慢闪，请短按设备任意开关键进行配对').exists(timeout=30):
                            break
                # 命名设备
                print("点击配对")
                if self.device(text='设备此时蓝灯慢闪，请短按设备任意开关键进行配对').exists(timeout=60):
                    time.sleep(2)
                    try:
                        self.ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.ser.write(bytes.fromhex('A0 01 00 A1'))
                        if self.device(resourceId='com.govee.home:id/done').exists(timeout=60):
                            pass
                        else:
                            subprocess.call(['adb', 'shell', 'am', 'force-stop', 'com.govee.home'])
                            time.sleep(2)
                            self.device.app_start('com.govee.home')
                            continue
                        old_time = datetime.now()
                        add_device_num += 1
                        print("配对次数：", add_device_num)
                        self.get_log.info("配对次数：{}".format(add_device_num))
                    except Exception as e:
                        print("继电器串口错误：", e)
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
                        if self.device(resourceId="com.govee.home:id/iv_setting").exists(timeout=60):
                            break
                elif self.device(text='ASUS_F0_2G').exists(timeout=60):
                    self.device(resourceId="com.govee.home:id/et_pwd").clear_text()
                    self.device(resourceId="com.govee.home:id/et_pwd").send_keys("govee123")
                    self.device(resourceId="com.govee.home:id/send_wifi").click_exists(timeout=30)
                if self.device(resourceId='com.govee.home:id/iv_switch').exists(timeout=180):
                    add_success_num += 1
                    print("配对配网成功，次数：", add_success_num)
                    self.get_log.info("配对配网成功，次数：{}".format(add_success_num))
                    new_time = datetime.now()
                    now_time = new_time - old_time
                    print("配网时长：", now_time)
                    self.get_log.info("配网时长：{}".format(now_time))
                    if add_device_num == 1000:
                        print("测试完成")
                        break
                if self.device(resourceId="com.govee.home:id/iv_setting").exists(timeout=30):
                    self.device(resourceId="com.govee.home:id/iv_setting").click_exists(timeout=30)
                    """ 删除设备 """
                    time.sleep(2)
                    self.down()
                    time.sleep(2)
                    while True:
                        self.device(resourceId="com.govee.home:id/tv4BtnDelete").click_exists(timeout=30)
                        time.sleep(2)
                        print("删除")
                        if self.device(resourceId="com.govee.home:id/btn_done").exists(timeout=30):
                            time.sleep(2)
                            break

                    self.device(resourceId="com.govee.home:id/btn_done").click_exists(timeout=30)
                    time.sleep(5)
            except Exception as e:
                print(e)

    # ble压测
    def in_page(self, sku_list):
        for in_sku in sku_list:
            while True:
                try:
                    self.device(text=in_sku).click_exists(timeout=5)
                    old_time = datetime.now()
                    if self.device(resourceId='com.govee.home:id/iv_switch').exists(timeout=30):
                        new_time = datetime.now()
                        self.in_page_num += 1
                        in_time = new_time - old_time
                        self.get_log.info(
                            "{0} wifi弱网进入详情页用时：[{1}][第{2}次]".format(in_sku, in_time, self.in_page_num))
                        print("{0} wifi弱网进入详情页用时：[{1}][第{2}次]".format(in_sku, in_time, self.in_page_num))
                        self.device(resourceId='com.govee.home:id/iv_back').click_exists(timeout=30)
                        time.sleep(5)
                        if self.in_page_num == 1000:
                            print("测试结束")
                            break
                    else:
                        while True:
                            self.device(text=in_sku).click_exists(timeout=5.0)
                            if self.enter_device(in_sku):
                                break
                            else:
                                time.sleep(5)
                    # self.get_log.info("第{0}次".format(self.in_page_num))
                except Exception:
                    pass

    # 开关压测
    def on_off_test(self, on_off_list):
        on_off_num = 0
        for i in on_off_list:
            print(i)
            self.device(text=i).click_exists(timeout=10)
            while True:
                # self.ser.write(bytes.fromhex('A0 01 01 A2'))
                # time.sleep(1)
                # self.ser.write(bytes.fromhex('A0 01 00 A1'))
                # time.sleep(3)
                # self.ser.write(bytes.fromhex('A0 01 01 A2'))
                # time.sleep(1)
                # self.ser.write(bytes.fromhex('A0 01 00 A1'))
                self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=30)
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=30)
                on_off_num += 1
                time.sleep(2)
                print("{0}开关测试次数：{1}".format(i, on_off_num))
                self.get_log.info("{0}开关测试次数：{1}".format(i, on_off_num))
                if on_off_num == 1000:
                    self.get_log.info("测试结束")
                    self.device(resourceId='com.govee.home:id/iv_back').click_exists(timeout=30)
                    on_off_num = 0
                    time.sleep(5)
                    break

    # ota压测
    def ota_test(self):
        time_start = 0
        ota_num = 0
        time_end = 0
        while True:
            try:
                date_line = self.ser.readline().decode()
                # time.sleep(0.1)
                print(date_line)
                # self.write_txt(self.txt_date)
                while True:
                    if '"percent":"0"' in date_line:
                        time.sleep(time_start + 0.02)  # 每次断电间隔时间加0.02s
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                        print("设备在开始OTA下载后{0}秒断电".format(time_start))
                        self.get_log.info("设备在开始OTA下载后{0}秒断电".format(time_start))
                        time.sleep(3)
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                        print("停止时间：{0}".format(time_start))
                        ota_num += 1
                        print('"设备在开始OTA下载后断电{0}次"'.format(ota_num))
                        self.get_log.info('"设备在开始OTA下载后断电{0}次"'.format(ota_num))
                    elif '"percent":"100"' in date_line:
                        time.sleep(0.1)
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                        time.sleep(3)
                        self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(0.5)
                        self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                        ota_num += 1
                        break
                    else:
                        break
                if ota_num == 1000:
                    print("测试结束")
                    break
            except Exception as e:
                print(e)

    # 恢复出厂压测
    def factory_test(self):
        factory_num = 0
        while True:
            try:
                self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
                time.sleep(10)
                self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
                time.sleep(30)
                factory_num += 1
                print("恢复出厂测试次数：", factory_num)
                self.get_log.info("恢复出厂测试次数：{0}".format(factory_num))
                if factory_num == 1000:
                    self.get_log.info("测试结束")
                    break
            except Exception:
                pass

    # 进入详情页验证
    def enter_device(self, sku=None):
        if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=30):
            print("进入详情页")
            self.in_page_num += 1
            self.get_log.info("进入{0}详情页成功".format(sku))
            return True
        else:
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/iv_back").click_exists(timeout=5.0)
                print("{0}30秒还未进入详情页，连接设备失败，退出详情页".format(sku))
                self.get_log.info("{0}30秒还未进入详情页，连接设备失败，退出详情页".format(sku))
            except Exception as e:
                print(e)
            return False

    def down(self):
        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                          0.1 * self.height)  # 向下滑动


if __name__ == '__main__':
    handle_H5086 = H5086('com9', 'com7', 115200, 9600, 1)  # com为串口日志，com1为继电器
    test_list = ['Smart Plug Pro8', 'Smart Plug Pro4', 'Smart Plug Pro5', 'Smart Plug Pro3', 'Smart Plug Pro1']
    while True:
        # handle_H5086.on_off_test()  # 开关压测
        # handle_H5086.in_page(test_list)  # ble压测
        # handle_H5086.add_devise_devices()  # 配网压测
        # handle_H5086.factory_test()   # 恢复出厂压测
        # handle_H5086.on_off_test(test_list)  # 开关机压测
        handle_H5086.ota_test()  # 开关机压测
