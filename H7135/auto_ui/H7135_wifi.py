#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 单机压测
import datetime
import time

import serial
import uiautomator2 as u2

from H7142.get_log.get_log import GetLog


class H7135Test:
    def __init__(self, com, dbs, timeout):
        self.test_count = 100
        self.err_test_count=0
        self.com = com
        self.dbs = dbs
        self.timeout = timeout
        self.device = u2.connect_usb('d5cd8968')
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\H7135_Auto\get_log\H7135_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H7135'
        try:
            self.ser = serial.Serial(self.com,
                                     self.dbs,
                                     timeout=self.timeout)
            print("*********打开串口成功*********")
        except Exception as e:
            print("*********串口异常:{}*********".format(e))
            self.err = -1

    # 写入数据
    # def write_date(self, write_itme):
    #     print(hex(write_itme))
        # self.ser.write(write_itme.hex())
    def turn_on_relay(self):
        self.ser.write(bytes.fromhex('A0 01 01 A2'))
        time.sleep(1)
        self.ser.write(bytes.fromhex('A0 01 00 A1'))
        time.sleep(5)

    # 下滑
    def down(self):
        self.device.swipe(0.5 * self.width, 0.7 * self.height, 0.5 * self.width,
                          0.3 * self.height)  # 向下滑动

    # 上滑
    def up(self):
        self.device.swipe(0.5 * self.width, 0.1 * self.height, 0.5 * self.width,
                          0.9 * self.height)  # 向上滑动

    def start_test(self):
        # 调用函数控制继电器开关
        n = 0
        print("开启成功")
        # 判断当前是否需要进入详情页
        try:
            # program.ui.resultBrowser.append("添加设备/删除设备自动化测试中------>第{}次".format(n + 1))
            # try:
            """添加设备"""
            # 添加”+“
            self.device(resourceId="com.govee.home:id/ivDevAdd").click_exists(timeout=5)
            # 输入要添加的SKU
            self.device(resourceId="com.govee.home:id/tv_search").click_exists(timeout=5)
            time.sleep(2)
            self.device(resourceId="com.govee.home:id/et_search").send_keys(self.sku)
            time.sleep(1)
            # 点击SKU
            # self.device(resourceId="com.govee.home:id/sku_des").click_exists(timeout=2)
            # 选择设备
            self.device.xpath('//*[@resource-id="com.govee.home:id/device_list"]/android.widget.RelativeLayout[1]').click_exists(timeout=5)
            # self.device(resourceId="com.govee.home:id/tvGuideConfirm").click_exists(timeout=5)
            self.device.xpath('//*[@resource-id="com.govee.home:id/device_list"]/android.widget.RelativeLayout[1]').click_exists(timeout=10)
            time.sleep(10)
            self.turn_on_relay()
            self.start_update_time = datetime.datetime.now()  # 开始升级时间
            # 命名设备
            self.device(resourceId="com.govee.home:id/done").click_exists(timeout=2)
            # wifi配置
            # self.device(resourceId="et_pwd").clear()
            # self.device(resourceId="et_pwd").send_keys("20170201")
            self.device(resourceId="com.govee.home:id/send_wifi").click_exists(timeout=2)
            time.sleep(20)
            # wifi_success_toast = "设备Wi-Fi连接成功"  # toast弹窗
            toast = self.device.toast.get_message(180.0, 10.0, 'message').encode('utf-8').decode()
            print(toast)
            if self.device(resourceId="com.govee.home:id/iv_gear_high_icon").wait(timeout=180):
                print("配网成功")
                success_time = datetime.datetime.now()  # 升级成功结束时间
                all_time = success_time - self.start_update_time
                self.get_log.info("升级成功，用时：{}".format(all_time))

            """ 删除设备 """
            # 点击设备设置按钮
            self.device(resourceId="com.govee.home:id/btn_setting").click_exists(timeout=60)
            for i in range(2):
                self.down()  # 下滑
            self.down()  # 下滑
            self.device(resourceId= "com.govee.home:id/btn_delete").click_exists(timeout=5)
            self.device(resourceId= "com.govee.home:id/btn_done").click_exists(timeout=5)
            time.sleep(5)
            # self.err_test_count += 1
            # n += 1
            # if n == self.test_count:
            #     self.logs.info("测试完成！")
            #     success_count = self.test_count - self.err_test_count  # 成功次数
            #     success_rate = success_count / self.test_count  # 成功率
            #     self.logs.info("测试完成！共测试{}次,成功{}次,成功率{:.2%}".format(self.test_count, success_count, success_rate))

        except Exception as e:
            print(e)




if __name__ == '__main__':
    test = H7135Test('com28', 9600, 3)
    n = 1
    while True:
        test.start_test()
