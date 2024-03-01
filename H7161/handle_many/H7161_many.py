#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 挂机测试
import time
import uiautomator2 as u2

from H7161.get_log.get_log import GetLog


class H7161Test:
    def __init__(self):
        self.device = u2.connect_usb('d5cd8968')   # 小米10
        # self.device = u2.connect_usb('424e4d504c383098')  # 三星
        self.device.app_start('com.govee.home')
        self.device.click_post_delay = 1 # 点击后1s延迟
        # 场景
        # self.scene = ['Mosrning', 'Heat Around a Fireplace', 'Creek', 'Good Night Kiss', 'Night Light']
        self.scene = ['Morning', 'Heat Around a Fireplace', 'Creek', 'Good Night Kiss', 'Night Light', 'Meditation',
                      'Firework'
                      ' Party', 'Deep Thought', 'Rainbow Bubble', 'Autumn Rain Hitting Leaves', 'Space Walk',
                      'Crossing the Field']
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\H7161_Auto\handle_many\log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()

    def start_test(self):
        for sc in range(12):  # 1-5个场景
            for dev in range(1, 7):  # 1-6号机
                try:
                    self.device(text=dev).click_exists(timeout=10)
                except Exception as e:
                    print("定位出错了：", e)
                # time.sleep(1)
                if self.check_connect():
                    # 判断是否弹窗提示72h清洗
                    if self.device(text='知道了').exists(timeout=3):
                        self.device(text='知道了').click(timeout=3)
                    flag = self.device(resourceId='com.govee.home:id/container_mode_atmosphere_default').info['enabled']
                    if flag:  # 如果设备处于可点击状态
                        self.device(resourceId='com.govee.home:id/container_mode_atmosphere_default').click_exists(timeout=5)
                        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width, 0.1 * self.height)
                        # time.sleep(1)
                        self.device(resourceId='com.govee.home:id/iv_more').click_exists(timeout=5)  # 点击更多
                        # time.sleep(1)
                        try:
                            # 场景
                            self.device(text=self.scene[sc]).click()
                            self.get_log.info("{0}号机切换到{1}成功！".format(dev, self.scene[sc]))
                            print("{0}号机切换到{1}成功！".format(dev, self.scene[sc]))
                            # time.sleep(1)
                        except Exception as e:
                            self.get_log.info("{0}号机切换到{1}失败！".format(dev, self.scene[sc]))
                            print("{0}号机切换到{1}失败！".format(dev, self.scene[sc]))
                            # time.sleep(1)
                        self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=5)
                        time.sleep(5)
                    else:
                        print("{0}号机关机或缺水！无法切换预设".format(dev))
                        self.get_log.info("{0}号机关机或缺水！无法切换预设".format(dev))
                        self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=5)
                        time.sleep(5)
                else:
                    while True:
                        self.device(text=dev).click_exists(timeout=5)
                        # time.sleep(1)
                        if self.check_connect():
                            break
                        else:
                            time.sleep(5)

    # 检测是否连接成功
    def check_connect(self):
        if self.device(resourceId="com.govee.home:id/iv_switch").wait(timeout=10.0):
            print("连接成功")
            return True
        else:
            print("连接失败")
            self.get_log.info('10秒wifi还没连接上，设备详情页加载失败')
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                self.get_log.info('退出详情页')
            except Exception as e:
                print(e)
            return False


if __name__ == '__main__':
    test = H7161Test()
    while True:
        test.start_test()
        time.sleep(10)
