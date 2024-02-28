#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : alexa

import time
import uiautomator2 as u2

from Alexa_Google.get_log import GetLog


class GoogleTest:
    def __init__(self):
        self.device = u2.connect_usb('d5cd8968')  # 小米10
        self.device.click_post_delay = 1  # 点击后1s延迟
        # device = u2.connect_usb('424e4d504c383098')  # 三星
        self.device.app_start('com.youdao.dict')
        self.device.click_post_delay = 1  # 点击后1s延迟
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\H7161_Auto\handle_many\log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        # 曲目
        self.music = [
            # "Alexa.turn on lily",
            # "Alexa.set Lily to custom",  # 自定义、预设
            # "Alexa.set Lily mist to Low","Alexa.set Lily mist to High",
            # "Alexa.set Lily White Noise to bird song", "Alexa.set Lily White Noise to Bonfire",
            # "Alexa.set Lily White Noise to Chirp", "Alexa.set Lily White Noise to Clock",
            "Alexa.set Lily White Noise to Falling leaves", "Alexa.set Lily White Noise to Fireworks",
            "Alexa.set Lily White Noise to Happy Tune", "Alexa.set Lily White Noise to Little Star",
            "Alexa.set Lily White Noise to Soft Misic", "Alexa.set Lily White Noise to River",
            "Alexa.set Lily White Noise to Lullaby", "Alexa.set Lily White Noise to Universe",
            "Alexa.set Lily White Noise to Thunder", "Alexa.set Lily White Noise to Little Train",
            "Alexa.set Lily White Noise to Water Drop", "Alexa.set Lily White Noise to Waterfall",
            "Alexa.set Lily White Noise to Wave", "Alexa.set Lily White Noise to Wind bell",
            "Alexa.set Lily White Noise to Wind",
            "Alexa.set White Noise Volume of Lily to 1 ", "Alexa.set White Noise Volume of Lily to 100 ",  # 调节音量
            "Alexa.set Lily White Noise to close",  # 关闭白噪音
            "Alexa.set Lily White Noise Volume to 1 ", "Alexa.set Lily White Noise Volume to 100 ",  # 调节音量
            'Alexa.set Lily white noise volume to medium', 'Alexa.set Lily white noise volume to low',  # 音量高中低
            'Alexa.set Lily white noise volume to high',
            "Alexa.turn off light of Lily", 'Alexa.turn on light of Lily',  # 开关夜灯
            "Alexa.set Lily to scene",
            "Alexa.set Lily to custom",  # 自定义、预设
            'Alexa.set Lily mist to close',  # 关雾
            'Alexa.enable light on lily',
            'Alexa.disable light on lily',
            "Alexa.turn off lily",
        ]

    def start_music(self):
        try:
            self.device(resourceId="com.youdao.dict:id/search_container").click()
            self.device(resourceId="com.youdao.dict:id/et_search_enter").click()
            self.device.xpath('com.youdao.dict:id/et_search_enter').set_text(self.music[0])
            self.device(resourceId="com.youdao.dict:id/tv_word").click()
            self.device(resourceId="com.youdao.dict:id/iv_translate_origin_pronounce").click()
            time.sleep(20)
            self.device(resourceId="com.youdao.dict:id/et_search_enter").clear_text()
            for i in range(1, len(self.music)):
                self.device.xpath('com.youdao.dict:id/et_search_enter').set_text(self.music[i])
                self.device(resourceId="com.youdao.dict:id/tv_word").click()
                self.device(resourceId="com.youdao.dict:id/iv_translate_origin_pronounce").click()
                time.sleep(10)
                self.device(resourceId="com.youdao.dict:id/et_search_enter").clear_text()
            self.device.xpath(
                '//*[@resource-id="com.youdao.dict:id/fl_back_arrow_bt"]/android.widget.ImageView[1]').click()
        except Exception as e:
            print(e)
            self.device.xpath('//*[@resource-id="com.youdao.dict:id/fl_back_arrow_bt"]/android.widget.ImageView[1]').click()


if __name__ == '__main__':
    run = GoogleTest()
    n=0
    while True:
        run.start_music()
        n+=1
        print("测试了{}次".format(n))

