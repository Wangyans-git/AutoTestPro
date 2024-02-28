#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 操作app
import datetime
import os
import time

import allure
import pytest

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By


# from GoveeTest_H7131.package_pytest.process_serial import program


@allure.epic("APP自动化测试")
class TestH7131(object):
    # test_count_7 = 0
    # test_count_9 = 0
    # test_count_7 = 0
    # test_count_9 = 0
    # 每个类前执行
    def setup_class(self):
        self.driver = start_app.start_appium()
        # return self.driver

    # 判断设备是否通电
    def t_or_f(self, element):
        source = self.driver.page_source
        if element in source:
            return True
        else:
            return False

    @allure.feature("进入设备7详情页")
    def test_app_7(self):
        # self.driver = start_app.start_appium()
        try:
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("设备7")').click()
            print("\n--------进入设备详情页--------")
            time.sleep(2)

        except Exception as e:
            print("找不到详情页元素了！！！\n", e)
            TouchAction(self.driver).press(x=90, y=170).release().perform()
            # self.start_appium()
        if self.t_or_f("重新连接"):
            TouchAction(self.driver).press(x=90, y=170).release().perform()  # 无法通过id定位就通过定位坐标
            time.sleep(2)
            # 等待10s重新进入详情页
            while True:
                self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("设备7")').click()
                time.sleep(2)
                if self.t_or_f("重新连接"):
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                else:
                    break
            # 如果不能点击切换模式按钮
            if self.driver.find_element(By.ID, 'iv_gear_icon').is_enabled() is not True:
                try:
                    self.driver.find_element(By.ID, 'iv_switch').click()
                    print("设备7开机成功")
                    time.sleep(2)
                except Exception as e:
                    print("找不到开关元素了！！！\n", e)
                try:
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("找不到返回元素了！！！\n", e)
            else:
                time.sleep(2)
                try:
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("找不到返回元素了！！！\n", e)
        # 如果不能点击切换模式按钮
        else:
            if self.driver.find_element(By.ID, 'iv_gear_icon').is_enabled() is not True:

                try:
                    self.driver.find_element(By.ID, 'iv_switch').click()
                    print("设备7开机成功")
                    time.sleep(2)
                except Exception as e:
                    print("找不到开关元素了！！！\n", e)
                try:
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("找不到返回元素了！！！\n", e)
            else:
                time.sleep(2)
                try:
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("找不到返回元素了！！！\n", e)
                time.sleep(2)

    @allure.feature("进入设备9详情页")
    def test_app_9(self):
        # global test_count_9
        try:
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("设备9")').click()
            print("\n--------进入设备详情页--------")
            time.sleep(2)
        except Exception as e:
            print("找不到详情页元素了！！！\n", e)
            TouchAction(self.driver).press(x=90, y=170).release().perform()
            # self.start_appium()
        if self.t_or_f("重新连接"):
            TouchAction(self.driver).press(x=90, y=170).release().perform()  # 无法通过id定位就通过定位坐标
            time.sleep(2)
            # 等待10s重新进入详情页
            while True:
                self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("设备9")').click()
                time.sleep(2)
                if self.t_or_f("重新连接"):
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                else:
                    break
            # 如果不能点击切换模式按钮
            if self.driver.find_element(By.ID, 'iv_gear_icon').is_enabled() is not True:
                try:
                    self.driver.find_element(By.ID, 'iv_switch').click()
                    print("设备9开机成功")
                    time.sleep(2)
                except Exception as e:
                    print("找不到开关元素了！！！\n", e)
                try:
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("找不到返回元素了！！！\n", e)
            else:
                time.sleep(2)
                try:
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("找不到返回元素了！！！\n", e)
        # 如果不能点击切换模式按钮
        else:
            if self.driver.find_element(By.ID, 'iv_gear_icon').is_enabled() is not True:

                try:
                    self.driver.find_element(By.ID, 'iv_switch').click()
                    print("设备9开机成功")
                    time.sleep(2)
                except Exception as e:
                    print("找不到开关元素了！！！\n", e)
                try:
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("找不到返回元素了！！！\n", e)
            else:
                time.sleep(2)
                try:
                    TouchAction(self.driver).press(x=90, y=170).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("找不到返回元素了！！！\n", e)
        print("等待60秒")
        time.sleep(60)

    # @allure.feature("进入对比6详情页")
    # def test_app_6(self):
    #     test_count = 0
    #     try:
    #         self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("对比6")').click()
    #         print("\n--------进入设备详情页--------")
    #         time.sleep(2)
    #     except Exception as e:
    #         print("找不到详情页元素了！！！\n", e)
    #         # self.start_appium()
    #     if self.t_or_f("重新连接"):
    #         TouchAction(self.driver).press(x=90, y=170).release().perform()  # 无法通过id定位就通过定位坐标
    #         time.sleep(15)
    #         # 等待10s重新进入详情页
    #         while True:
    #             self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("对比6")').click()
    #             time.sleep(2)
    #             if self.t_or_f("重新连接"):
    #                 TouchAction(self.driver).press(x=90, y=170).release().perform()
    #                 time.sleep(15)
    #             else:
    #                 break
    #         # 如果不能点击切换模式按钮
    #         if self.driver.find_element(By.ID, 'iv_gear_icon').is_enabled() is not True:
    #             try:
    #                 self.driver.find_element(By.ID, 'iv_switch').click()
    #                 test_count += 1
    #                 print("对比6一共开机了{}次".format(test_count))
    #                 time.sleep(2)
    #             except Exception as e:
    #                 print("找不到开关元素了！！！\n", e)
    #             try:
    #                 TouchAction(self.driver).press(x=90, y=170).release().perform()
    #                 time.sleep(15)
    #             except Exception as e:
    #                 print("找不到返回元素了！！！\n", e)
    #         else:
    #             time.sleep(2)
    #             try:
    #                 TouchAction(self.driver).press(x=90, y=170).release().perform()
    #                 time.sleep(2)
    #             except Exception as e:
    #                 print("找不到返回元素了！！！\n", e)
    #     # 如果不能点击切换模式按钮
    #     else:
    #         if self.driver.find_element(By.ID, 'iv_gear_icon').is_enabled() is not True:
    #
    #             try:
    #                 self.driver.find_element(By.ID, 'iv_switch').click()
    #                 test_count += 1
    #                 print("对比6一共开机了{}次".format(test_count))
    #                 time.sleep(2)
    #             except Exception as e:
    #                 print("找不到开关元素了！！！\n", e)
    #             try:
    #                 TouchAction(self.driver).press(x=90, y=170).release().perform()
    #                 time.sleep(2)
    #             except Exception as e:
    #                 print("找不到返回元素了！！！\n", e)
    #         else:
    #             time.sleep(2)
    #             try:
    #                 TouchAction(self.driver).press(x=90, y=170).release().perform()
    #                 time.sleep(2)
    #             except Exception as e:
    #                 print("找不到返回元素了！！！\n", e)
    #     print("等待150秒")
    #     time.sleep(150)


    # def teardown_class(self):
    #     os.system("allure serve C:\\wys\\AutoTestProjects\\GoveeTest_H7131\\report\\report")
    #     os.system("allure generate GoveeTest_H7131/report/report -o GoveeTest_H7131/report/report_result/ --clean")

    def start_appium(self):
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '11',
            # 'deviceName': "424e4d504c383098",  # 三星
            'deviceName': "d5cd8968",  # 小米10
            'appPackage': 'com.govee.home',
            'appActivity': 'com.govee.home.main.MainTabActivity',
            'noReset': 'true',  # 启动app时不要清除app里原有的数据
        }
        try:
            driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
            driver.implicitly_wait(180)
            if driver:
                print("\n*********Appium服务器启动成功*********\n")
            return driver
        except Exception as e:
            print("\n*********Appium服务器错误*********\n", e)
            return False

    # 获取手机屏幕宽度
    def get_size(self):
        # 获取窗口尺寸
        size = self.driver.get_window_size()
        x = size['width']
        y = size['height']
        return x, y

    # 向下滑动
    def swipe_down(self):

        size = self.get_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.9)
        y2 = int(size[1] * 0.1)
        self.driver.swipe(x1, y1, x1, y2, 500)

    # 向上滑动
    def swipe_up(self):

        size = self.get_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.1)
        y2 = int(size[1] * 0.9)
        self.driver.swipe(x1, y1, x1, y2, 500)


start_app = TestH7131()
