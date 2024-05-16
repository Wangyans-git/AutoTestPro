#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 2024/4/10 14:40
# @Author  : yansheng.wang
# @File    : handle_upgrade.py
# @Description : H5100 OTA压测


import time
from pathlib import Path

import uiautomator2 as u2

from H5100.log import get_log


class H5100Test:
    def __init__(self):
        self.device = u2.connect_usb('')
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)
        # 脚本日志
        FILE = Path(__file__).resolve()
        ROOT = FILE.parents[1]  # YOLOv5 root directory
        path = str(Path(ROOT) / f"H5100/log/OTA配网压测.txt")
        print(path)
        self.get_log = get_log.GetLog(path)
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.update_success_num = 0

    def start_test(self):
        while True:
            try:
                if self.device(text="重新扫描").exists(timeout=5):
                    self.device(text="重新扫描").click_exists(timeout=5)
                if self.device(text="温度报警").exists(timeout=60):
                    for i in range(3):
                        self.down()
                    if self.device(text="固件版本").exists(timeout=10):
                        while True:
                            self.device(text="固件版本").click_exists(timeout=5)
                            if self.device(resourceId="com.govee.home:id/btn_update").exists():
                                break
                        time.sleep(1)
                        while True:
                            self.device(resourceId="com.govee.home:id/btn_update").click_exists(timeout=10)
                            if self.device(text="设备升级").exists(timeout=5):
                                self.get_log.info('开始升级')
                                break
                        self.check_update_ok()
                        while True:
                            self.device(text="完成").click_exists(timeout=10)
                            if not self.device(text="完成").exists(timeout=5):
                                break
                else:
                    self.get_log.info('超过60秒设备未连接上，设备设置页加载失败')
            except Exception as e:
                print("出错:", e)

    # 检测是否连接成功
    def check_connect(self):
        if self.device(resourceId="com.govee.home:id/btn_setting").wait(timeout=10.0):
            return True
        else:
            self.get_log.info('超过10秒设备未连接上，设备详情页加载失败')
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                self.get_log.info('退出详情页')
            except Exception as e:
                print(e)
            return False

    # 检查是否升级成功
    def check_update_ok(self):
        update_success_toast = "升级成功"  # toast弹窗
        update_fail_toast = "蓝牙断开连接，升级失败"  # toast弹窗
        toast = self.device.toast.get_message(180.0, 10.0, 'message').encode('utf-8').decode()
        # print(toast)
        if toast == update_success_toast:
            self.update_success_num += 1
            print("升级成功")
            self.get_log.info(f"升级成功{self.update_success_num}次")
        elif toast == update_fail_toast:
            print("蓝牙断开连接，升级失败")
            self.get_log.info("蓝牙断开连接，升级失败")

    def down(self):
        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                          0.1 * self.height)  # 向下滑动


if __name__ == '__main__':
    test = H5100Test()
    test.start_test()
