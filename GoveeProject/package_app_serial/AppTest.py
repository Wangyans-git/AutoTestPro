#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 2022/07/18
# @Author  :yansheng.wang 王衍升
# @File    : AppTest
# @Description : 被SerialTest调用控制app

from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction

import time


class ExecuteApp(object):

    def __init__(self):
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '11',
            # 'deviceName': "424e4d504c383098",  # 三星
            'deviceName': "d5cd8968",  # 小米10
            'appPackage': 'com.govee.home',
            'appActivity': 'com.govee.home.HomeActivity',
            'automationName': 'Uiautomator2',
            'noReset': 'true',  # 启动app时不要清除app里原有的数据
            'adbExecTimeout': 200000,
            'newCommandTimeout': 36000,
        }
        try:
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
            self.driver.implicitly_wait(30)
        except Exception as e:
            print("Appium服务器错误！！！\n", e)

    # 配网
    def add_device(self):
        try:
            # 添加”+“
            self.driver.find_element(By.ID, "iv_add").click()
            time.sleep(2)
            # 输入要添加的SKU
            self.driver.find_element(By.ID, "tv_search").click()
            time.sleep(3)
            self.driver.find_element(By.ID, "et_search").send_keys("H7131")
            time.sleep(3)
            # 点击SKU
            self.driver.find_element(By.ID, "sku_des").click()
            # 选择设备
            time.sleep(8)
            self.driver.find_elements(By.CLASS_NAME, "android.widget.RelativeLayout")[0].click()
            time.sleep(2)
            print("############################")
            print("等待配对(点击设备开关按钮。)")
            print("############################")
            time.sleep(10)
            # 命名设备
            self.driver.find_element(By.ID, "done").click()
            time.sleep(2)
            # wifi配置
            self.driver.find_element(By.ID, "et_pwd").clear()
            self.driver.find_element(By.ID, "et_pwd").send_keys("20170201")
            self.driver.find_element(By.ID, "send_wifi").click()
            time.sleep(20)
        except Exception as e:
            print("找不到元素了！！！\n", e)

    # 删除设备
    def del_device(self):
        try:
            # 点击设备设置按钮
            TouchAction(self.driver).press(x=1000, y=150).release().perform()  # 通过定位坐标
            time.sleep(2)
            self.swipe_down()  # 下滑
            self.driver.find_element(By.ID, "btn_delete").click()
            time.sleep(2)
            self.driver.find_element(By.ID, "btn_done").click()
            time.sleep(5)
        except Exception as e:
            print("找不到元素了！！！\n", e)

    # 进入app详情页
    def app_home(self):
        try:
            self.driver.find_element(By.ID, "rl_item").click()
            time.sleep(5)
        except Exception as e:
            print("找不到元素了！！！\n", e)

    # 控制设备详情页头部上半部分功能
    def app_top(self):
        try:
            # 点击开关
            self.driver.find_element(By.ID, "iv_switch").click()
            time.sleep(3)
            self.driver.find_element(By.ID, "iv_switch").click()
            time.sleep(3)
            # 低挡
            self.driver.find_element(By.ID, "iv_gear_low_bg").click()
            time.sleep(3)
            # 中挡
            self.driver.find_element(By.ID, "iv_gear_mid_bg").click()
            time.sleep(3)
            # 高档
            self.driver.find_element(By.ID, "iv_gear_high_icon").click()
            time.sleep(3)
            # 自动挡
            self.driver.find_element(By.ID, "iv_auto_icon").click()
            time.sleep(3)
            # 风扇挡
            self.driver.find_element(By.ID, "iv_fan_icon").click()
            time.sleep(3)
        except Exception as e:
            print("找不到元素了！！！\n", e)

    # 控制设备详情页头部下半部分功能
    def app_down(self):
        try:
            # 摇头
            self.driver.find_element(By.ID, 'iv_shake_switch').click()
            time.sleep(3)
            self.driver.find_element(By.ID, 'iv_shake_switch').click()
            time.sleep(3)
            # 夜灯
            self.driver.find_element(By.ID, 'iv_light_rgb_switch_ext1').click()
            time.sleep(3)
            self.driver.find_element(By.ID, 'iv_light_rgb_switch_ext1').click()
            time.sleep(3)
            # 锁
            self.driver.find_element(By.ID, 'iv_lock_switch').click()
            time.sleep(3)
            self.driver.find_element(By.ID, 'iv_lock_switch').click()
            time.sleep(3)
            # 显示
            self.driver.find_element(By.ID, 'iv_light_indicator_switch').click()
            time.sleep(3)
            self.driver.find_element(By.ID, 'iv_light_indicator_switch').click()
            time.sleep(3)
            # 绑定温湿度计
            self.driver.find_element(By.ID, 'bind_tempe_container').click()
            time.sleep(3)
            self.driver.find_element(By.ID, "item_icon_choose_iv").click()
            time.sleep(3)
            self.driver.find_element(By.ID, "btn_ok").click()  # 定位该id会导致手机界面下拉设置框
            time.sleep(10)
            # 删除温湿度计
            self.driver.find_element(By.ID, 'iv_bind_temperature_arrow').click()
            time.sleep(3)
            self.driver.find_element(By.ID, 'btn_delete').click()
            time.sleep(3)
            self.driver.find_element(By.ID, 'btn_done').click()
            time.sleep(3)
        except Exception as e:
            print("找不到元素了！！！\n", e)

    # 获取手机屏幕宽度
    def get_size(self):
        # 获取窗口尺寸
        size = self.driver.get_window_size()
        x = size['width']
        y = size['height']
        return x, y

    def swipe_down(self):
        # 向下滑动
        size = self.get_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.9)
        y2 = int(size[1] * 0.1)
        self.driver.swipe(x1, y1, x1, y2, 500)

    def swipe_up(self):
        # 向上滑动
        size = self.get_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.1)
        y2 = int(size[1] * 0.9)
        self.driver.swipe(x1, y1, x1, y2, 500)


run = ExecuteApp()
