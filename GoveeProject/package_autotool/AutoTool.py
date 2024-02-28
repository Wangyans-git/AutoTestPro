#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 自动化测试工具
import json
import sys

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtUiTools import QUiLoader

import serial
import threading
import time
import datetime

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By


class App(QWidget):

    def __init__(self, dbs, timeout):
        super().__init__()
        self.err = 0
        self.dbs = dbs
        self.timeout = timeout
        # self.active = True  # 启停标志位

        self.err_date = ''  # 做是否有错误判断的数据
        self.txt_date = ''  # 写入TXT的数据
        self.err_count = 0  # 记录错误次数
        self.ui = QUiLoader().load('Skutest.ui')

        # self.ui.setMinimumSize(570, 700)
        # self.ui.setMaximumSize(570, 700)
        self.ui.mucButton.clicked.connect(self.button_mcu)  # 单选mcu测试
        self.ui.appButton.clicked.connect(self.button_app)  # 单选app自动化测试时
        self.ui.mcuBox.clicked.connect(self.mcu_func)  # 复选MCU功能
        self.ui.add_deviceBox.clicked.connect(self.add_device_func)  # 复选添加设备功能
        self.ui.add_tempBox.clicked.connect(self.add_temp_func)  # 复选绑定温湿度计功能

        self.ui.quitButton.clicked.connect(self.quit_app)  # 退出
        # self.ui.stopButton.clicked.connect(self.stop_run)  # 暂停

        # 默认设置
        self.ui.mucButton.setChecked(True)  # 默认设置为MCU
        self.ui.add_deviceBox.setEnabled(False)  # 禁用设备按钮
        self.ui.add_tempBox.setEnabled(False)  # 禁用温湿度计按钮



    """
    MCU模块
    """

    # 单选mcu测试
    def button_mcu(self):
        self.ui.add_deviceBox.setEnabled(False)  # 禁用设备按钮
        self.ui.add_deviceBox.setChecked(False)  # 取消设备按钮选择
        self.ui.add_tempBox.setEnabled(False)  # 禁用温湿度计按钮
        self.ui.mcuBox.setEnabled(True)  # 使能MCU
        self.ui.add_tempBox.setChecked(False)  # 取消温湿度计按钮选择
        self.ui.mcuTextEdit.setEnabled(True)  # 可输入mcu指令

    # 单选app测试
    def button_app(self):
        # 选择app后，所有功能选项使能，但是mcu指令输入界面灰显
        self.ui.add_deviceBox.setEnabled(True)  # 添加设备使能
        self.ui.add_tempBox.setEnabled(True)  # 绑定温湿度计使能
        self.ui.mcuBox.setEnabled(False)  # MCU灰显
        self.ui.mcuBox.setChecked(False)  # 取消设备按钮选择
        self.ui.mcuTextEdit.setEnabled(False)

    # 复选MCU
    def mcu_func(self):
        try:
            com = self.ui.serialEdit.text()  # 串口
            self.ser = serial.Serial(com,
                                     # self.ser = serial.Serial('com8',
                                     self.dbs,
                                     timeout=self.timeout)
            self.ui.resultBrowser.append("*********连接串口成功*********")
            self.ui.mucButton.setEnabled(False)
            self.ui.appButton.setEnabled(False)
        except Exception:
            self.ui.resultBrowser.append("*********端口号错误或者未填写端口号*********")
            self.ui.resultBrowser.append("*********需要重新打开程序*********")
            # self.ui.mcuBox.setEnabled(True)
            self.err = -1
        if self.ui.mcuBox.isChecked():
            self.ui.mcuBox.setEnabled(False)
            self.ui.pushButton.clicked.connect(self.thread_send)
            self.ui.pushButton.clicked.connect(self.thread_recv)

    """
    Appium模块
    """

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

    # 复选app添加设备
    def add_device_func(self):
        try:
            com = self.ui.serialEdit.text()  # 串口
            self.ser = serial.Serial(com,
                                     # self.ser = serial.Serial('com8',
                                     self.dbs,
                                     timeout=self.timeout)
            self.ui.resultBrowser.append("*********连接串口成功*********")
            self.ui.mcuBox.setEnabled(False)
            self.ui.mucButton.setEnabled(False)
            self.ui.appButton.setEnabled(False)
        except Exception:
            self.ui.resultBrowser.append("*********端口号错误或者未填写端口号*********")
            self.ui.resultBrowser.append("*********需要重新打开程序*********")
            # self.ui.mcuBox.setEnabled(True)
            self.err = -1
        if self.ui.add_deviceBox.isChecked():
            self.ui.add_tempBox.setEnabled(False)  # 绑定温湿度计灰显
            self.ui.add_deviceBox.setEnabled(False)  # 绑定温湿度计灰显
            self.ui.pushButton.clicked.connect(self.thread_recv)  # 断言判断
            self.ui.pushButton.clicked.connect(self.thread_add_devices)  # appium启动配置

    # 复选app绑定温湿度计
    def add_temp_func(self):
        try:
            com = self.ui.serialEdit.text()  # 串口
            self.ser = serial.Serial(com,
                                     # self.ser = serial.Serial('com8',
                                     self.dbs,
                                     timeout=self.timeout)
            self.ser.open()
            self.ui.resultBrowser.append("*********连接串口成功*********")
            self.ui.mucButton.setEnabled(False)
            self.ui.appButton.setEnabled(False)
        except Exception:
            self.ui.resultBrowser.append("*********端口号错误或者未填写端口号*********")
            self.ui.resultBrowser.append("*********需要重新打开程序*********")
            # self.ui.mcuBox.setEnabled(True)
            self.err = -1
        if self.ui.add_tempBox.isChecked():
            self.ui.add_deviceBox.setEnabled(False)  # 添加设备灰显
            self.ui.add_tempBox.setEnabled(False)  # 添加设备灰显
            self.ui.pushButton.clicked.connect(self.thread_recv)  # 断言判断
            self.ui.pushButton.clicked.connect(self.thread_add_temp)  # appium启动配置

    # app执行添加设备
    def add_devices(self):
        self.ui.add_deviceBox.setEnabled(False)  # 添加/删除设备灰显
        self.ui.pushButton.setEnabled(False)  # 开始测试灰显
        n = 0
        err_test_count = 0
        test_count = self.ui.countEdit.text()
        if test_count != 0 and test_count != "":
            self.ui.resultBrowser.append("===========开始测试===========")
            desired_caps = {
                'platformName': 'Android',
                'platformVersion': '11',
                # 'deviceName': "424e4d504c383098",  # 三星
                'deviceName': "d5cd8968",  # 小米10
                'appPackage': 'com.govee.home',
                'appActivity': 'com.govee.home.HomeActivity',
                'autoAcceptAlerts': 'true',  # 默认选择接受弹窗的条款
                'noReset': 'true',  # 启动app时不要清除app里原有的数据
            }
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
            self.driver.implicitly_wait(30)
            while n < int(test_count):
                self.ui.resultBrowser.append("添加设备/删除设备自动化测试中------>第{}次".format(n + 1))
                try:
                    """添加设备"""
                    # 添加”+“
                    self.driver.find_element(By.ID, "ivDevAdd").click()
                    time.sleep(2)
                    # 输入要添加的SKU
                    self.driver.find_element(By.ID, "tv_search").click()
                    time.sleep(3)
                    self.driver.find_element(By.ID, "et_search").send_keys("H7143")
                    time.sleep(2)
                    # 点击SKU
                    self.driver.find_element(By.ID, "sku_des").click()
                    # 选择设备
                    time.sleep(8)
                    self.driver.find_elements(By.CLASS_NAME, "android.widget.RelativeLayout")[0].click()
                    time.sleep(2)
                    self.ui.resultBrowser.append("等待配对(点击设备开关按钮。)")
                    time.sleep(10)
                    # 命名设备
                    self.driver.find_element(By.ID, "done").click()
                    time.sleep(2)
                    # wifi配置
                    self.driver.find_element(By.ID, "et_pwd").clear()
                    self.driver.find_element(By.ID, "et_pwd").send_keys("20170201")
                    self.driver.find_element(By.ID, "send_wifi").click()
                    time.sleep(20)

                    """ 删除设备 """
                    # 点击设备设置按钮
                    TouchAction(self.driver).press(x=1000, y=150).release().perform()  # 通过定位坐标
                    time.sleep(2)
                    self.swipe_down()  # 下滑
                    self.driver.find_element(By.ID, "btn_delete").click()
                    time.sleep(2)
                    self.driver.find_element(By.ID, "btn_done").click()
                    time.sleep(5)
                except Exception:
                    self.ui.resultBrowser.append("找不到定位元素了..")
                    err_test_count += 1
                n += 1
                if n == test_count:
                    self.ui.resultBrowser.append("测试完成！")
                    success_count = test_count - err_test_count  # 成功次数
                    success_rate = success_count / test_count  # 成功率
                    self.ui.resultBrowser.append(
                        "测试完成！共测试{}次,成功{}次,成功率{:.2%}".format(test_count, success_count, success_rate))
                    self.ui.pushButton.setEnabled(True)  # 开始测试使能
        else:
            self.ui.resultBrowser.append("输入测试次数...")
            self.ui.pushButton.setEnabled(True)  # 开始测试使能
            self.ui.add_deviceBox.setEnabled(True)  # 添加设备使能使能

    # app执行绑定温湿度计
    def add_temp(self):
        self.ui.add_tempBox.setEnabled(False)  # 添加/删除设备灰显
        self.ui.pushButton.setEnabled(False)  # 开始按钮设备灰显
        self.ui.resultBrowser.append("\r")
        n = 0
        err_test_count = 0
        test_count = self.ui.countEdit.text()
        if test_count != 0 and test_count != "":
            self.ui.resultBrowser.append("===========开始测试app===========")
            desired_caps = {
                'platformName': 'Android',
                'platformVersion': '11',
                # 'deviceName': "424e4d504c383098",  # 三星
                'deviceName': "d5cd8968",  # 小米10
                'appPackage': 'com.govee.home',
                'appActivity': 'com.govee.home.HomeActivity',
                'autoAcceptAlerts': 'true',  # 默认选择接受弹窗的条款
                'noReset': 'true',  # 启动app时不要清除app里原有的数据
            }
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
            self.driver.implicitly_wait(120)
            while n < int(test_count):
                self.ui.resultBrowser.append("绑定温湿度计/删除温湿度计自动化测试中------>第{}次".format(n + 1))
                try:
                    # 进入设备详情页
                    self.driver.find_element(By.ID, "com.govee.home:id/rl_item").click()
                    time.sleep(5)
                    self.swipe_down()
                    # 绑定温湿度计
                    self.driver.find_element(By.ID, 'container_top_bind').click()
                    time.sleep(3)
                    self.driver.find_element(By.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android"
                                             ".widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayou"
                                             "t/android.widget.RelativeLayout/android.widget.RelativeLayout/androidx.re"
                                             "cyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.w"
                                             "idget.ImageView[2]").click()
                    time.sleep(3)
                    self.driver.find_element(By.ID, "btn_ok").click()
                    time.sleep(10)
                    # 删除温湿度计
                    self.driver.find_element(By.ID, 'iv_bind_temperature_arrow').click()
                    time.sleep(3)
                    self.driver.find_element(By.ID, 'btn_delete').click()
                    time.sleep(3)
                    self.driver.find_element(By.ID, 'btn_done').click()
                    time.sleep(3)
                except Exception:
                    self.ui.resultBrowser.append("找不到定位元素了..")
                    err_test_count += 1
                n += 1
                if n == test_count:
                    self.ui.resultBrowser.append("测试完成！")
                    success_count = test_count - err_test_count  # 成功次数
                    success_rate = success_count / test_count  # 成功率
                    self.ui.resultBrowser.append(
                        "测试完成！共测试{}次,成功{}次,成功率{:.2%}".format(test_count, success_count, success_rate))
                    self.ui.pushButton.setEnabled(True)  # 添加/删除设备正常
        else:
            self.ui.resultBrowser.append("输入测试次数...")
            self.ui.pushButton.setEnabled(True)  # 开始测试使能
            self.ui.add_tempBox.setEnabled(True)  # 添加设备使能使能

    """
    线程控制app
    """

    # app添加设备
    def thread_add_devices(self):
        try:
            self.add_devices_thread = threading.Thread(target=self.add_devices)
            self.add_devices_thread.start()
        except Exception as e:
            print("无法启动线程:{}".format(e))

    # app绑定温湿度计
    def thread_add_temp(self):
        try:
            self.add_temp_thread = threading.Thread(target=self.add_temp)
            self.add_temp_thread.start()
        except Exception as e:
            print("无法启动线程:{}".format(e))

    """
        线程输入mcu指令，读取串口数据
    """

    # 输入mcu指令
    def thread_send(self):
        try:
            self.send_thread = threading.Thread(target=self.mcu_run)
            self.send_thread.start()
        except Exception as e:
            print("无法启动线程:{}".format(e))

    # 线程读取数据
    def thread_recv(self):
        try:
            self.recv_thread = threading.Thread(target=self.read_date)
            self.recv_thread.start()
        except Exception as e:
            print("无法启动线程:{}".format(e))

    # 退出
    def quit(self):
        self.add_devices_thread.join()
        self.add_temp_thread.join()
        self.send_thread.join()
        self.recv_thread.join()
    """
        数据处理
    """

    # 退出
    @staticmethod
    def quit_app():
        sys.exit()

    # 写入数据
    def write_date(self, write_itme):
        self.ui.pushButton.setEnabled(False)  # 测试开始后开始测试按钮灰置
        self.ser.write(write_itme.encode())

    # 判断错误数据
    def date_result(self, n):
        date = self.err_date.split('.')
        if len(date) - 1 == len(n):  # 因为split分隔后会多一段数据，所以-1
            self.err_date = ''
        elif len(date) == 1:
            pass
        else:
            err_ = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S前的一次执行中有错误！！！"))
            self.txt_date += err_
            App.write_txt(self.txt_date)
            print(err_)
            self.err_date = ''
            self.err_count += 1
        return self.err_count

    # 数据写入txt文档
    @staticmethod
    def write_txt(t):
        result = str(t)
        try:
            with open('log.txt', 'w') as file_handle:
                file_handle.write(result)
        except Exception as e:
            print("文件读写出错：", e)

    # 处理串口数据，接收串口返回数据
    def read_date(self):
        check_edit = self.ui.assertTextEdit.toPlainText().split(",")
        check_dates = {}  # 断言数据
        while True:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S----->")
            is_success_date = ''  # 判断是否执行成功的临时数据
            try:
                date_line = self.ser.readline().decode()
                time.sleep(0.1)
                is_success_date += date_line
                self.txt_date += str(date_line)  # 所有写入到txt文档
                App.write_txt(self.txt_date)
                for i in range(len(check_edit)):
                    # 开机:55 11 01 00 01 01 69, 关机:55 11 01 00 01 00 68
                    check_dates[check_edit[i].split(":")[0]] = check_edit[i].split(":")[1]  # 将每个输入的键值对加入到字典里
                    check_list = []
                    for j in check_dates:
                        check_list.append(j)
                    if check_dates[check_list[i]] in date_line:
                        success_date = str(now_time + check_list[i]) + "."
                        self.err_date += success_date
                        self.txt_date += success_date
                        self.ui.resultBrowser.append(success_date)
            except Exception:
                break
        # else:
        #     self.ui.resultBrowser.append("请输入断言数据")

    # 测试muc主程序，串口输入mcu指令
    def mcu_run(self):
        if self.err == 0:
            m = 0  # 统计测试次数
            send_list = []  # 将MCU数据放入列表中遍历输入
            mcu_text = self.ui.mcuTextEdit.toPlainText().split(',')
            # print("mcu_text", self.ui.mcuTextEdit.toPlainText())
            for i in range(len(mcu_text)):
                send_list.append(mcu_text[i] + '\r')
            test_count = self.ui.countEdit.text()  # 测试的次数
            if test_count == '' and test_count == 0:
                self.ui.resultBrowser.append("输入测试次数...")
            elif self.ui.mcuTextEdit.toPlainText() != "" and self.ui.assertTextEdit.toPlainText() == "":
                self.ui.resultBrowser.append("请输入断言数据")
            elif self.ui.mcuTextEdit.toPlainText() == "" and self.ui.assertTextEdit.toPlainText() != "":
                self.ui.resultBrowser.append("请输入mcu指令")
            elif self.ui.mcuTextEdit.toPlainText() == "" and self.ui.assertTextEdit.toPlainText() == "":
                self.ui.resultBrowser.append("请输入mcu指令")
                self.ui.resultBrowser.append("请输入断言数据")
            elif self.ui.assertTextEdit.toPlainText() != "" and self.ui.assertTextEdit.toPlainText() != "":  # 都不为空才开始测试
                self.ui.resultBrowser.append("*********开启读取数据*********")
                while True:
                    try:
                        self.ui.resultBrowser.append("========第{}次测试开始========".format(m + 1))
                        for i in range(len(send_list)):
                            program.write_date(send_list[i])  # 写入MCU数据
                            time.sleep(3)
                        self.ui.resultBrowser.append("========第{}次测试完成========".format(m + 1))
                        program.date_result(send_list)
                        m += 1
                        if m == int(test_count):
                            self.ui.resultBrowser.append("所有测试完成,一共测试了{}次,出现了{}次错误".format(m, program.
                                                                                           date_result(send_list)))
                            self.ui.pushButton.setEnabled(True)  # 所有测试完成后开始测试按钮恢复功能
                            break
                    except Exception as e:
                        print(e)
                        break


if __name__ == '__main__':
    app = QApplication([])
    program = App(115200, 1)
    app.setWindowIcon(QIcon("./touxiang.ico"))
    program.ui.show()
    app.exec_()
