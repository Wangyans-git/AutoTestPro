#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 单机压测
import time
import uiautomator2 as u2

from H7142.get_log.get_log import GetLog


class H7140Test:
    def __init__(self):
        self.device = u2.connect_usb()
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\H7140_Auto\get_log\H7140_log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.sku = 'H7148'

    def start_test(self):
        # 判断当前是否需要进入详情页
        if self.device(text=self.sku).wait(timeout=5.0):
            self.device(text=self.sku).click_exists(timeout=5.0)
            time.sleep(5)
            if self.check_connect():
                try:
                    # 判断是否弹窗提示72h清洗
                    if self.device(resourceId='com.govee.home:id/btn_done').exists(timeout=3):
                        self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=5.0)
                    # 判断设备是否是关机状态，如果是就先开机
                    flag = self.device(resourceId='com.govee.home:id/iv_gear_icon').info['enabled']  # 开机状态
                    # print(flag)
                    if flag:  # 如果设备处于可点击状态
                        while True:
                            """
                            切换出雾档位
                            """
                            self.device(resourceId='com.govee.home:id/iv_gear_icon').click(timeout=5.0)  # 手动挡
                            if self.check_connect():
                                self.get_log.info("切换至手动挡位成功！")
                                print("切换至手动挡位成功！")
                                # 出雾级别
                                self.device.click(0.162, 0.776)  # 1档
                                self.device.click(0.488, 0.776)  # 5档
                                self.device.click(0.827, 0.776)  # 9档
                                if self.device(resourceId='com.govee.home:id/btn_done').exists(timeout=3):
                                    self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=5.0)
                                if self.check_connect():
                                    self.get_log.info("切换挡位成功！")
                                    print('切换挡位成功！')
                                else:
                                    self.get_log.error("切换档位后连接失败！")
                                    print("切换档位后连接失败！")
                            else:
                                self.get_log.error("切换至手动挡位后连接失败！")
                                print("切换至手动挡位后连接失败！")
                            """
                            切换自定义模式
                            """
                            self.device(resourceId='com.govee.home:id/iv_custom_icon').click(timeout=5)
                            if self.check_connect():
                                self.get_log.info("切换至自定义模式成功！")
                                print('切换至自定义模式成功！')
                            else:
                                self.get_log.error("切换自定义模式后连接失败！")
                                print("切换自定义模式后连接失败")
                            """
                            切换自动模式
                            """
                            self.device(resourceId='com.govee.home:id/iv_auto_icon').click(timeout=5)
                            # 如果有确认弹窗，点击取消
                            if self.device(resourceId='com.govee.home:id/btn_cancel').wait(timeout=5):
                                self.device(resourceId='com.govee.home:id/btn_cancel').click(timeout=5)
                            if self.check_connect():
                                self.get_log.info("切换至自动模式成功！")
                                print("切换至自动模式成功")
                            else:
                                self.get_log.error("切换自动模式后连接失败！")
                                print("切换自动模式后连接失败")
                    elif self.device(resourceId='com.govee.home:id/iv_switch').info['enabled'] is False:  # 如果开关不可点击，表示已缺水
                        # self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5)
                        self.get_log.error("设备缺水,测试结束")
                        n = 0
                        # print("返回：",n)
                        return n
                    else:
                        self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5)
                        self.get_log.info("设备关机过，重新开机测试..")
                        print("设备关机过，重新开机测试..")
                except Exception as e:
                    print(e)
                else:
                    if self.device(resourceId='com.govee.home:id/btn_cancel').wait(timeout=5):
                        self.device(resourceId='com.govee.home:id/btn_cancel').click(timeout=5)
                        print("又有弹窗了，哪里来的？")
            else:
                while True:
                    self.device(text=self.sku).click_exists(timeout=5.0)
                    if self.check_connect():
                        break
                    else:
                        time.sleep(5)
        else:
            print("没有改找到该设备名的设备!")

    # 检测是否连接成功
    def check_connect(self):
        if self.device(resourceId="com.govee.home:id/iv_switch").wait(timeout=10.0):
            return True
        else:
            self.get_log.error('10秒wifi还没连接上，设备详情页加载失败')
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                print("退出详情页")
                self.get_log.info('退出详情页')
            except Exception as e:
                print(e)
            return False


if __name__ == '__main__':
    test = H7140Test()
    n = 1
    while True:
        test.start_test()
        if test.start_test() == 0:
            print("设备缺水,测试结束")
            break
