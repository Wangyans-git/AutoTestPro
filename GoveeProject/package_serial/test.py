#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :yansheng.wang
# @File    :
# @Description : 单机压测
import random
import subprocess
import time

import schedule
import uiautomator2 as u2

# from H7142.get_log.get_log import GetLog

# class H7135Test:
#     def __init__(self):
#         self.device = u2.connect_usb("d5cd8968")
#         self.device.app_start('com.govee.home')
#         self.device.implicitly_wait(30)  # 元素等待时间30s
#         self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
#         # 脚本日志
#         self.get_log = GetLog("H7135_log.log")
#         # 获取手机分辨率
#         self.width, self.height = self.device.window_size()
#         self.sku = 'H7136'
#
#     def start_test(self):
#         # 判断当前是否需要进入详情页
#         if self.device(text=self.sku).wait(timeout=5.0):
#             self.device(text=self.sku).click_exists(timeout=5.0)
#             time.sleep(5)
#             n = 0
#             while True:
#                 if self.check_connect():
#                     try:
#                         # self.logs.info('退出详情页')
#                         if n % 2 == 1:
#                             self.device(resourceId='com.govee.home:id/iv_gear_low_icon').click_exists(timeout=5.0)
#                             self.get_log.info("低档")
#                             self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#                             self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#
#                             n += 1
#                             time.sleep(1)
#                         elif n % 2 == 0:
#                             self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').click_exists(timeout=5.0)
#                             self.get_log.info("中档")
#                             self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#                             self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#
#                             n += 1
#                             time.sleep(1)
#                         # elif n % 5 == 3:
#                         #     self.device(resourceId='com.govee.home:id/iv_gear_high_icon').click_exists(timeout=5.0)
#                         #     self.get_log.info("高档")
#                         #     self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#                         #     self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#                         #     n += 1
#                         #     time.sleep(1)
#                         # elif n % 5 == 4:
#                         #     self.device(resourceId='com.govee.home:id/iv_fan_icon').click_exists(timeout=5.0)
#                         #     self.get_log.info("风扇档")
#                         #     self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#                         #     self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#                         #     n += 1
#                         #     time.sleep(1)
#                         # elif n % 5 == 0:
#                         #     self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
#                         #     self.get_log.info("自动档")
#                         #     self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#                         #     self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
#                         #     n += 1
#                         #     time.sleep(1)
#                         # # 判断设备是否是关机状态，如果是就先开机
#                         # flag = self.device(resourceId='com.govee.home:id/iv_delay_off_arrow').info['enabled']  # 开机状态
#                         # # print(flag)
#                         # if flag:  # 如果设备处于可点击状态
#                         #     """
#                         #     切换档位
#                         #     """
#                         #     if self.check_connect():
#                         #         self.logs.info("切换至手动挡位成功！")
#                         #         print("切换至手动挡位成功！")
#                         #         # 出雾级别
#                         #         self.device(resourceId='com.govee.home:id/iv_gear_low_icon').click_exists(timeout=5.0)  # 低档
#                         #         self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').click_exists(timeout=5.0)  # 中档
#                         #         self.device(resourceId='com.govee.home:id/iv_gear_high_icon').click_exists(timeout=5.0)  # 高档
#                         #         self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)  # 自动档
#                         #         self.device(resourceId='com.govee.home:id/iv_fan_icon').click_exists(timeout=5.0)  # 风档
#                         #
#                         #         if self.device(resourceId='com.govee.home:id/btn_done').exists(timeout=3):
#                         #             self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=5.0)
#                         #         if self.check_connect():
#                         #             self.logs.info("切换挡位成功！")
#                         #             print('切换挡位成功！')
#                         #         else:
#                         #             self.logs.error("切换档位后连接失败！")
#                         #             print("切换档位后连接失败！")
#                         #     else:
#                         #         self.logs.error("切换至手动挡位后连接失败！")
#                         #         print("切换至手动挡位后连接失败！")
#                         # else:
#                         #     self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5)
#                         #     self.logs.info("设备关机过，重新开机测试..")
#                         #     print("设备关机过，重新开机测试..")
#
#                     except Exception as e:
#                         print(e)
#                     else:
#                         if self.device(resourceId='com.govee.home:id/btn_cancel').exists():
#                             self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=2)
#                             self.get_log.info("又有弹窗了，哪里来的？")
#                         elif self.device(resourceId='com.govee.home:id/dialog_done').exists():
#                             self.device(resourceId='com.govee.home:id/dialog_done').click_exists(timeout=2)
#                             self.get_log.info("又有弹窗了，哪里来的？")
#                         elif self.device(resourceId='com.govee.home:id/btn_done').exists():
#                             self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=2)
#                             self.get_log.info("又有弹窗了，哪里来的？")
#                         else:
#                             pass
#                 else:
#                     while True:
#                         self.device(text=self.sku).click_exists(timeout=5.0)
#                         if self.check_connect():
#                             break
#                         else:
#                             time.sleep(5)
#         else:
#             print("没有改找到该设备名的设备!")
#
#     # 检测是否连接成功
#     def check_connect(self):
#         if self.device(resourceId="com.govee.home:id/iv_switch").wait(timeout=10.0):
#             return True
#         else:
#             self.get_log.error('10秒wifi还没连接上，设备详情页加载失败')
#             # 退出详情页
#             try:
#                 self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
#                 print("退出详情页")
#                 # self.logs.info('退出详情页')
#             except Exception as e:
#                 print(e)
#             return False


hour = random.randint(9, 9)
minute = random.randint(15, 25)

# 格式化为时间字符串
random_time = "{:02d}:{:02d}".format(hour, minute)


# print(random_time)


def run_test():
    try:
        device = u2.connect_usb()
        # device.shell("input keyevent 26")
        time.sleep(3)
        device.app_start('com.alibaba.android.rimet')
        time.sleep(5)
        device(resourceId="com.alibaba.android.rimet:id/cb_privacy").click_exists(timeout=10)
        device(resourceId="com.alibaba.android.rimet:id/ll_next").click_exists(timeout=10)
        device(text="其他方式登录").click_exists(timeout=10)
        device(text="密码登录").click_exists(timeout=10)
        device(resourceId="com.alibaba.android.rimet:id/et_pwd_input").click_exists(timeout=10)
        time.sleep(1)
        device(resourceId="com.alibaba.android.rimet:id/et_pwd_input").send_keys("govee123")
        device(resourceId="com.alibaba.android.rimet:id/btn_confirm").click_exists(timeout=10)
        time.sleep(1)
        device(resourceId="com.alibaba.android.rimet:id/cb_privacy").click_exists(timeout=10)
        time.sleep(1)
        time.sleep(120)
        subprocess.call(['adb', 'shell', 'am', 'force-stop', 'com.alibaba.android.rimet'])
        time.sleep(3)
        device.shell("input keyevent 26")
        device.implicitly_wait(130)
    except Exception as e:
        print(e)


def open_servers():
    try:
        device = u2.connect_usb()
        # device.shell("input keyevent 26")
        time.sleep(2)
        device.app_start('com.govee.home')
        time.sleep(3)
        device(text="设备").click_exists(timeout=10)
        device(text="自动化").click_exists(timeout=10)
        print("点击")
        time.sleep(2)
    except Exception as e:
        print(e)


# run_test()
def my_task():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    run_test()
    # 连接设备


scheduler = schedule.Scheduler()

# scheduler.every().day.at(random_time).do(my_task)
scheduler.every().day.at("09:22").do(my_task)

n = 0
# 无限循环，直到任务执行
while True:
    scheduler.run_pending()
    print(n)
    if n % 10 == 0:
        open_servers()
    n += 1
    time.sleep(30)
