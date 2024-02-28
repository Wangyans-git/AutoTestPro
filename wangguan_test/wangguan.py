#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 单机压测
import datetime
import time
import uiautomator2 as u2
import subprocess
from PIL import Image, ImageChops, ImageGrab
import os
import cv2


from H7142.get_log.get_log import GetLog


class H7135Test:
    def __init__(self):
        # self.device = u2.connect_usb('d5cd8968')
        self.device = u2.connect_usb()
        # self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        self.device.settings['operation_delay'] = (0, 1)  # 每次点击后等待2s
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\H7135_Auto\get_log\H7135_log.log")
        # 获取手机分辨率
        # self.width, self.height = self.device.window_size()
        # self.sku = 'H7135'
        # 设置截图保存路径
        self.save_path = './error_iamge/'

        # 创建空白图片对象（作为累加结果）
        self.result_image = Image.new('RGB', (0, 0))

    def calculate(self,p3):
        try:
            image1 = cv2.imread('./p1.png')  # 原图第一排机器
            # image2 = cv2.imread('./p2.png')   # 原图第二排机器
            # 灰度直方图算法
            # 计算单通道的直方图的相似值
            hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
            hist3 = cv2.calcHist([p3], [0], None, [256], [0.0, 255.0])   # 对比图

            # hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
            # hist4 = cv2.calcHist([p4], [0], None, [256], [0.0, 255.0])  # 对比图
            # 计算直方图的重合度
            degree1 = 0
            for i in range(len(hist1)):
                if hist1[i] != hist3[i]:
                    degree1 = degree1 + (1 - abs(hist1[i] - hist3[i]) / max(hist1[i], hist3[i]))
                else:
                    degree1 = degree1 + 1
            degree1 = degree1 / len(hist1)

            # 计算直方图的重合度
            # degree2 = 0
            # for i in range(len(hist2)):
            #     if hist2[i] != hist2[i]:
            #         degree2 = degree2 + (1 - abs(hist2[i] - hist4[i]) / max(hist2[i], hist4[i]))
            #     else:
            #         degree2 = degree2 + 1
            # degree2 = degree2 / len(hist2)
            return degree1
        except Exception as e:
            print(e)

    def jietu(self):
        # 截图
        # 指定要截取的区域
        start_x, start_y = 1, 350
        end_x, end_y = 1300, 750
        # 截取 App 屏幕指定区域
        result = self.device.screenshot(format='opencv')
        cropped_result = result[start_y:end_y, start_x:end_x]
        cv2.imwrite('p1.png', cropped_result)

        # start_x1, start_y1 = 1, 950
        # end_x1, end_y1 = 1300, 1150
        # # 截取 App 屏幕指定区域
        # result = self.device.screenshot(format='opencv')
        # cropped_result = result[start_y1:end_y1, start_x1:end_x1]
        # cv2.imwrite('p2.png', cropped_result)

    # 杀后台
    def start_test_kill(self):
        try:
            self.device.app_start('com.govee.home')
            time.sleep(2)
            subprocess.call(['adb', 'shell', 'am', 'force-stop', 'com.govee.home'])
            time.sleep(3)  # 等待5分钟
            self.device.app_start('com.govee.home')
            time.sleep(3)  # 等待5分钟
            # 截图
            # 指定要截取的区域
            start_x, start_y = 1, 350
            end_x, end_y = 1300, 750
            # 截取 App 屏幕指定区域
            result = self.device.screenshot(format='opencv')
            cropped_result = result[start_y:end_y, start_x:end_x]
            cv2.imwrite('p3.png', cropped_result)
            # 输出相似率
            image1 = cv2.imread('./p3.png')

            # 指定要截取的区域
            # start_x1, start_y1 = 1, 950
            # end_x1, end_y1 = 1300, 1150
            # # 截取 App 屏幕指定区域
            # result = self.device.screenshot(format='opencv')
            # cropped_result = result[start_y1:end_y1, start_x1:end_x1]
            # cv2.imwrite('p4.png', cropped_result)
            # # 输出相似率
            # image2 = cv2.imread('./p4.png')

            # image.save("p2.png", image)  # 或'home.png'，目前只支持png 和 jpg格式的图像
            # # 输出相似率
            # image2 = cv2.imread('./p2.png')
            # result = self.calculate(image1,image2)
            result = self.calculate(image1)
            print("相似度：", result)
            if result == 1:
                print("杀后台所有设备网络正常")
            else:
                now = datetime.datetime.now()
                timestamp = int(now.strftime("%H%M%S"))
                nowtime = now.strftime("%Y-%m-%d %H:%M:%S")
                image = self.device.screenshot()  # default format="pillow"
                image.save(f'{self.save_path}{timestamp}.png')  # 或'home.png'，目前只支持png 和 jpg格式的图像
                print("杀后台有设备wifi断开连接，已截图,时间:", nowtime)
            time.sleep(2)
        except Exception as e:
            print("杀掉后台后异常报错：",e)

    # 退出后台
    def start_test_quit(self):
        try:
            self.device.app_start('com.govee.home')
            time.sleep(2)
            self.device.press("home")
            time.sleep(3)  # 等待5分钟
            self.device.app_start('com.govee.home')
            time.sleep(3)  # 等待5分钟
            # 截图
            # 指定要截取的区域
            start_x, start_y = 1, 350
            end_x, end_y = 1300, 750
            # 截取 App 屏幕指定区域
            result = self.device.screenshot(format='opencv')
            cropped_result = result[start_y:end_y, start_x:end_x]
            cv2.imwrite('p3.png', cropped_result)
            # 输出相似率
            image1 = cv2.imread('./p3.png')

            # 指定要截取的区域
            # start_x1, start_y1 = 1, 950
            # end_x1, end_y1 = 1300, 1150
            # # 截取 App 屏幕指定区域
            # result = self.device.screenshot(format='opencv')
            # cropped_result = result[start_y1:end_y1, start_x1:end_x1]
            # cv2.imwrite('p4.png', cropped_result)
            # # 输出相似率
            # image2 = cv2.imread('./p4.png')

            # image.save("p2.png", image)  # 或'home.png'，目前只支持png 和 jpg格式的图像
            # # 输出相似率
            # image2 = cv2.imread('./p2.png')
            # result = self.calculate(image1, image2)
            result = self.calculate(image1)
            print("相似度：", result)
            if result == 1:
                print("退后台所有设备网络正常")
            else:
                now = datetime.datetime.now()
                timestamp = int(now.strftime("%H%M%S"))
                nowtime = now.strftime("%Y-%m-%d %H:%M:%S")
                image = self.device.screenshot()  # default format="pillow"
                image.save(f'{self.save_path}{timestamp}.png')  # 或'home.png'，目前只支持png 和 jpg格式的图像
                print("退后台有设备wifi断开连接，已截图,时间:", nowtime)
            print("===========================================")
            time.sleep(2)
        except Exception as e:
            print("退后台异常报错",e)


if __name__ == '__main__':
    test = H7135Test()
    # test.jietu()   # 截图
    n = 0
    while True:
        test.start_test_kill()
        test.start_test_quit()
        n+=1
        print(f"测试了{n}次")
