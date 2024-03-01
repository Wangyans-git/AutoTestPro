#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 单机压测
import time
import uiautomator2 as u2

from H7161.get_log.get_log import GetLog


class H7161Test:
    def __init__(self):
        self.device = u2.connect_usb('d5cd8968')
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)
        self.device.settings['operation_delay'] = (0, 3)  # 每次点击后等待2s
        self.scene = ['Morning', 'Heat Around a Fireplace', 'Creek', 'Good Night Kiss', 'Night Light','Meditation','Firework Party','Deep Thought']
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\H7161\handle_one\log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()

    def start_test(self):
        # 判断当前是否需要进入详情页
        if self.device(text='Smart Aroma Diffuser').wait(timeout=5.0):
            self.device(text='Smart Aroma Diffuser').click_exists(timeout=5.0)
            # self.device(text='5').click_exists(timeout=5.0)
            # 判断是否弹窗提示72h清洗
            if self.device(resourceId='com.govee.home:id/btn_done').exists(timeout=3):
                self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=5.0)
            if self.check_connect():
                # 选择预设模式
                try:
                    self.device(resourceId='com.govee.home:id/container_mode_atmosphere_default').click_exists(timeout=5.0)
                except Exception as e:
                    print("预设定位出错了：", e)
                    self.get_log.info("切换至预设模式失败！")
                try:
                    # 场景
                    for sc in range(8):  # 1-5个场景
                        self.device(text=self.scene[sc]).click_exists(timeout=5.0)
                        self.get_log.info("切换到{}成功！".format(self.scene[sc]))
                except Exception as e:
                    self.get_log.info("切换预设失败！")
                    print("切换预设定位失败：", e)
                # # 自定义
                # try:
                #     self.device(resourceId='com.govee.home:id/iv_custom_default_icon').click_exists(timeout=5.0)
                #     self.device(resourceId='com.govee.home:id/iv_max_fog_default_bg').click_exists(timeout=5.0)
                #     self.device(resourceId='com.govee.home:id/iv_min_fog_default_bg').click_exists(timeout=5.0)
                #     self.device.swipe(0.3 * self.width, 0.7 * self.height, 0.7 * self.width, 0.3 * self.height)
                #     self.device.xpath(
                #         '//*[@resource-id="com.govee.home:id/include_voice"]/android.widget.ImageView[3]').click_exists(
                #         timeout=5.0)
                #     self.device.xpath(
                #         '//*[@resource-id="com.govee.home:id/include_voice"]/android.widget.ImageView[2]').click_exists(
                #         timeout=5.0)
                #     self.device.xpath(
                #         '//*[@resource-id="com.govee.home:id/include_light"]/android.widget.ImageView[3]').click_exists(
                #         timeout=5.0)
                #     self.device.xpath(
                #         '//*[@resource-id="com.govee.home:id/include_light"]/android.widget.ImageView[2]').click_exists(
                #         timeout=5.0)
                #     self.device.swipe(0.3 * self.width, 0.3 * self.height, 0.7 * self.width, 0.7 * self.height)
                #     self.device(resourceId='com.govee.home:id/container_mode_atmosphere_default').click_exists(timeout=5.0)
                # except Exception as e:
                #     self.logs.info("切换自定义失败！")
                #     print("定位失败：", e)
            else:
                while True:
                    self.device(text='Smart Aroma Diffuser').click_exists(timeout=5.0)
                    if self.check_connect():
                        break
                    else:
                        time.sleep(5)

    # 检测是否连接成功
    def check_connect(self):
        if self.device(resourceId="com.govee.home:id/iv_switch").wait(timeout=10.0):
            print("进入详情页")
            self.get_log.info("进入详情页")
            return True
        else:
            self.get_log.info('10秒wifi还没连接上，设备详情页加载失败')
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                print("退出详情页")
                self.get_log.info('退出详情页')
            except Exception as e:
                print(e)
            return False


if __name__ == '__main__':
    test = H7161Test()
    while True:
        test.start_test()
