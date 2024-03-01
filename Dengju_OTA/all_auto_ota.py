#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 全部灯具OTA测试
import time
import uiautomator2 as u2
import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Dengju_OTA.get_log import GetLog


class H7161Test:
    def __init__(self):
        self.device = u2.connect_usb()
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\Dengju_OTA\log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        # 正常计数
        self.all_update_num_H6167 = 0
        self.all_update_num_H6078 = 0
        self.all_update_num_H6057 = 0
        self.all_update_num_H6052 = 0
        self.all_update_num_H1167 = 0
        self.all_update_num_H6092 = 0
        # 错误计数
        self.update_fail_num_H6167 = 0
        self.update_fail_num_H6078 = 0
        self.update_fail_num_H6057 = 0
        self.update_fail_num_H6052 = 0
        self.update_fail_num_H1167 = 0
        self.update_fail_num_H6092 = 0
        self.count = 0

    def start_test(self):
        # 点击全部开始，所有sku测试次数+1
        try:
            if self.device(resourceId='com.govee.home:id/tvUpdateAll').exists(timeout=60):
                self.device(resourceId='com.govee.home:id/tvUpdateAll').click_exists(timeout=5)
                # self.all_update_num_H6167 += 1
                self.all_update_num_H6078 += 1
                # self.all_update_num_H6057 += 1
                # self.all_update_num_H6052 += 1
                # self.all_update_num_H1167 += 1
                # self.all_update_num_H6092 += 1

                for i in range(1):
                    self.handle_pop()
                    toast = self.device.toast.get_message(120.0, 5.0, '2分钟内未升级完成或升级完成').encode('utf-8').decode()
                    print(toast)
                    time.sleep(5)
                    self.check_update_ok(toast)
                    if self.device(resourceId='com.govee.home:id/tvUpdateAll').exists():
                        break
                self.count += 1
                screenshot_path = fr'C:\wys\AutoTestProjects\Dengju_OTA\image\第{self.count}次全部升级后截图.png'
                self.device.screenshot(screenshot_path)
                self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width, 0.1 * self.height)  # 向下滑动
                screenshot_path1 = fr'C:\wys\AutoTestProjects\Dengju_OTA\image\第{self.count}次全部升级后下部分截图.png'
                self.device.screenshot(screenshot_path1)
                print("H6167成功{0}次，H6078成功{1}次，H6057成功{2}次,H6052成功{3},H1167成功{4},H6092成功{5}".format(
                    self.all_update_num_H6167,
                    self.all_update_num_H6078,
                    self.all_update_num_H6057,
                    self.all_update_num_H6052,
                    self.all_update_num_H1167,
                    self.all_update_num_H6092
                ))
                self.get_log.info("H6167成功{0}次，H6078成功{1}次，H6057成功{2}次,H6052成功{3},H1167成功{4},H6092成功{5}".format(
                    self.all_update_num_H6167,
                    self.all_update_num_H6078,
                    self.all_update_num_H6057,
                    self.all_update_num_H6052,
                    self.all_update_num_H1167,
                    self.all_update_num_H6092
                ))
                print("H6167失败{0}次，H6078失败{1}次，H6057失败{2}次,H6052失败{3},H1167失败{4},H6092失败{5}".format(
                    self.update_fail_num_H6167,
                    self.update_fail_num_H6078,
                    self.update_fail_num_H6057,
                    self.update_fail_num_H6052,
                    self.update_fail_num_H1167,
                    self.update_fail_num_H6092
                ))
                self.get_log.info("H6167失败{0}次，H6078失败{1}次，H6057失败{2}次,H6052失败{3},H1167失败{4},H6092失败{5}".format(
                    self.update_fail_num_H6167,
                    self.update_fail_num_H6078,
                    self.update_fail_num_H6057,
                    self.update_fail_num_H6052,
                    self.update_fail_num_H1167,
                    self.update_fail_num_H6092
                ))
                time.sleep(5)
                self.device(resourceId='com.govee.home:id/ivRefresh').click_exists(timeout=5)
                # self.device(resourceId='com.govee.home:id/iv_back').click_exists(timeout=5)
                time.sleep(30)
            else:
                self.device(resourceId='com.govee.home:id/ivRefresh').click_exists(timeout=5)
                # time.sleep(60)
        except Exception:
            print("报错")

    # 处理弹窗
    def handle_pop(self):
        time.sleep(10)
        if self.device(text='未连接到设备(H6167_04DE)，请在设备两米范围内重试').exists():
            # self.logs.info("Light Show Box超出蓝牙范围")
            self.all_update_num_H6167 -= 1
            print("H6167_04DE超出蓝牙范围")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='未连接到设备(H6078)，请在设备两米范围内重试').exists():
            self.all_update_num_H6078 -= 1
            print("H6078超出蓝牙范围")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='未连接到设备(H6057_7D93)，请在设备两米范围内重试').exists():
            self.all_update_num_H6057 -= 1
            # self.logs.info("Aura Table Lamp超出蓝牙范围")
            print("H6057_7D93超出蓝牙范围")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='未连接到设备(H6052-0830)，请在设备两米范围内重试').exists():
            self.all_update_num_H6052 -= 1
            # self.logs.info("H6601-B1A5超出蓝牙范围")
            print("H6052-0830超出蓝牙范围")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='未连接到设备(H1167)，请在设备两米范围内重试').exists():
            self.all_update_num_H1167 -= 1
            # self.logs.info("H6601-B1A5超出蓝牙范围")
            print("H1167超出蓝牙范围")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='未连接到设备(H6092-554E)，请在设备两米范围内重试').exists():
            self.all_update_num_H6092 -= 1
            # self.logs.info("H6601-B1A5超出蓝牙范围")
            print("H6092-554E超出蓝牙范围")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)

        # 失败的
        elif self.device(text='设备(H6167_04DE)连接中断，请重试').exists():
            # self.logs.info("Light Show Box超出蓝牙范围")
            self.all_update_num_H6167 -= 1
            print("H6167_04DE连接中断")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='设备(H6078)连接中断，请重试').exists():
            self.all_update_num_H6078 -= 1
            print("H6078连接中断")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='设备(H6057_7D93)连接中断，请重试').exists():
            self.all_update_num_H6057 -= 1
            # self.logs.info("Aura Table Lamp超出蓝牙范围")
            print("H6057_7D93连接中断")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='设备(H6052-0830)连接中断，请重试').exists():
            self.all_update_num_H6052 -= 1
            # self.logs.info("H6601-B1A5超出蓝牙范围")
            print("H6052-0830连接中断")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='设备(H1167)连接中断，请重试').exists():
            self.all_update_num_H1167 -= 1
            # self.logs.info("H6601-B1A5超出蓝牙范围")
            print("H1167连接中断")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)
        elif self.device(text='设备(H6092-554E)连接中断，请重试').exists():
            self.all_update_num_H6092 -= 1
            # self.logs.info("H6601-B1A5超出蓝牙范围")
            print("H6092-554E连接中断")
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=5)

    # 检查是否升级成功
    def check_update_ok(self, toast):
        # 计入升级失败的断言
        H6167_update_fail_toast = "该设备(H6167_04DE)升级失败，请开启蓝牙后重试"
        H6078_update_fail_toast = "该设备(H6078)升级失败，请开启蓝牙后重试"
        H6057_update_fail_toast = "该设备(H6057_7D93)升级失败，请开启蓝牙后重试"
        H6052_update_fail_toast = "该设备(H6052-0830)升级失败，请开启蓝牙后重试"
        H1167_update_fail_toast = "该设备(H1167)升级失败，请开启蓝牙后重试"
        H6092_update_fail_toast = "该设备(H6092-554E)升级失败，请开启蓝牙后重试"
        # 不计入升级失败的断言
        H6167_update_toast = "未连接到设备(H6167_04DE)，请在设备两米范围内重试"  # toast弹窗
        H6078_updat_toast = "未连接到设备(H6078)，请在设备两米范围内重试"  # toast弹窗
        H6057_update_toast = "未连接到设备(H6057_7D93)，请在设备两米范围内重试"  # toast弹窗
        H6052_update_toast = "未连接到设备(H6052-0830)，请在设备两米范围内重试"  # toast弹窗
        H1167_update_toast = "未连接到设备(H1167)，请在设备两米范围内重试"  # toast弹窗
        H6092_update_toast = "未连接到设备(H6092-554E)，请在设备两米范围内重试"  # toast弹窗

        H6167_update_toast1 = "设备(H6167_04DE)连接中断，请重试"  # toast弹窗
        H6078_updat_toast2 = "设备(H6078)连接中断，请重试"  # toast弹窗
        H6057_update_toast3 = "设备(H6057_7D93)连接中断，请重试"  # toast弹窗
        H6052_update_toast4 = "设备(H6052-0830)连接中断，请重试"  # toast弹窗
        H1167_update_toast5 = "设备(H1167)连接中断，请重试"  # toast弹窗
        H6092_update_toast6 = "设备(H6092-554E)连接中断，请重试"  # toast弹窗
        success_time = datetime.datetime.now()  # 升级成功结束时间
        # all_time = success_time - self.start_update_time
        # self.logs.info("升级成功，用时：{}".format(all_time))
        # 不计入失败
        if toast == H6167_update_toast:
            self.all_update_num_H6167 -= 1
            print("H6167超出蓝牙范围")
            # self.logs.info("Light Show Box超出蓝牙范围")
        elif toast == H6078_updat_toast or "":
            self.all_update_num_H6078 -= 1
            print('H6078超出蓝牙范围')
            # self.logs.info('Aura Table Lamp超出蓝牙范围')
        elif toast == H6057_update_toast:
            self.all_update_num_H6057 -= 1
            print("H6057超出蓝牙范围")
            # self.logs.info("6072-1784超出蓝牙范围")
        elif toast == H6052_update_toast:
            self.all_update_num_H6052 -= 1
            print("H6052超出蓝牙范围")
            # self.logs.info("6072-1784超出蓝牙范围")
        elif toast == H1167_update_toast:
            self.all_update_num_H1167 -= 1
            print("_H1167超出蓝牙范围")
            # self.logs.info("6072-1784超出蓝牙范围")
        elif toast == H6092_update_toast:
            self.all_update_num_H6092 -= 1
            print("H6092超出蓝牙范围")
            self.get_log.info("6072-1784超出蓝牙范围")

        elif toast == H6167_update_toast1:
            self.all_update_num_H6092 -= 1
            print("H6092超出蓝牙范围")
            self.get_log.info("6072-1784超出蓝牙范围")
        elif toast == H6078_updat_toast2:
            self.all_update_num_H6078 -= 1
            print('H6078超出蓝牙范围')
        elif toast == H6057_update_toast3:
            self.all_update_num_H6057 -= 1
            print("H6057超出蓝牙范围")
        elif toast == H6052_update_toast4:
            self.all_update_num_H6052 -= 1
            print("H6052超出蓝牙范围")
        elif toast == H1167_update_toast5:
            self.all_update_num_H1167 -= 1
            print("_H1167超出蓝牙范围")
        elif toast == H6092_update_toast6:
            self.all_update_num_H6092 -= 1
            print("H6092超出蓝牙范围")

        # 计入失败
        elif toast == H6167_update_fail_toast:
            self.update_fail_num_H6167 += 1
            print("H6167升级失败")
            # self.logs.info("H6167升级失败")
        elif toast == H6078_update_fail_toast:
            self.update_fail_num_H6078 += 1
            print("H6078升级失败")
            # self.logs.info("H6078 升级失败")
        elif toast == H6057_update_fail_toast:
            self.update_fail_num_H6057 += 1
            print("6057升级失败")
            # self.logs.info("6057升级失败")
        elif toast == H6052_update_fail_toast:
            self.update_fail_num_H6052 += 1
            print("H6052升级失败")
            # self.logs.info("H6052升级失败")
        elif toast == H1167_update_fail_toast:
            self.update_fail_num_H1167 += 1
            print("H1167升级失败")
            # self.logs.info("H1167升级失败")
        elif toast == H6092_update_fail_toast:
            self.update_fail_num_H6092 += 1
            print("H6092升级失败")
            # self.logs.info("H6092升级失败")


if __name__ == '__main__':
    test = H7161Test()
    while True:
        test.start_test()
