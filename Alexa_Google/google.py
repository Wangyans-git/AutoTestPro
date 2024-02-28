#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : Google
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
        # 场景
        # scene = ['Mosrning', 'Heat Around a Fireplace', 'Creek', 'Good Night Kiss', 'Night Light']
        # 脚本日志
        self.get_log = GetLog("C:\wys\AutoTestProjects\H7161_Auto\handle_many\log.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        # 曲目
        self.music = ["OK,Google.set Perry White Noise to bird song", "OK,Google.set Perry White Noise to Bonfire",
                      "OK,Google.set Perry White Noise to Chirp", "OK,Google.set Perry White Noise to Clock",
                      "OK,Google.set Perry White Noise to Falling leaves", "OK,Google.set Perry White Noise to Fireworks",
                      "OK,Google.set Perry White Noise to Happy Tune", "OK,Google.set Perry White Noise to Little Star",
                      "OK,Google.set Perry White Noise to Soft Misic", "OK,Google.set Perry White Noise to River",
                      "OK,Google.set Perry White Noise to Lullaby", "OK,Google.set Perry White Noise to Universe",
                      "OK,Google.set Perry White Noise to Thunder", "OK,Google.set Perry White Noise to Little Train",
                      "OK,Google.set Perry White Noise to Water Drop", "OK,Google.set Perry White Noise to Waterfall",
                      "OK,Google.set Perry White Noise to Wave", "OK,Google.set Perry White Noise to Wind bell",
                      "OK,Google.set Perry White Noise to Wind",
        # self.music = [
                      "OK,Google.set Perry Volume to 1 ", "OK,Google.set Perry Volume to 100 ",  # 调节音量
                      "OK,Google.set Perry to preset","OK,Google.set Perry to custom ",
                      "OK,Google.turn off perry night light","OK,Google.turn on perry night light",  # 开关夜灯
                      "OK,Google.set Perry to low", "OK,Google.set Perry to high",
                      "OK,Google.set Perry White Noise to close",  # 关闭白噪音
                      "OK,Google.set Perry mist to close",  # 关闭出雾
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


if __name__ == '__main__':
    run = GoogleTest()
    while True:
        run.start_music()
