#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 添加删除预设
import time
import uiautomator2 as u2


# from H7161.logs import GetLog


class H7161Test:
    def __init__(self):
        self.device = u2.connect_usb('d5cd8968')
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()

    # 添加预设
    def start_add(self):
        try:
            self.device(text='perry').click(timeout=3)
            time.sleep(1)
            self.device(resourceId='com.govee.home:id/iv_light_arrow').click(timeout=3)  # 场景编辑
            time.sleep(2)
            i = 0
            while True:
                self.device(resourceId='com.govee.home:id/btn_add').click(timeout=3)  # 添加按钮
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/tv_scenes_name').click(timeout=3)  # 场景名称
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/edit_name').click(timeout=3)  # 场景名称
                time.sleep(1)
                self.device.send_keys(str(i), clear=True)
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/btn_ok').click(timeout=3)
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/constraint_icon').click(timeout=3)  # 场景图标
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/btn_album').click(timeout=3)
                time.sleep(1)
                self.device.xpath(
                    '//*[@resource-id="com.govee.home:id/recyclerview"]/android.widget.FrameLayout[5]/android.view.View[2]').click(
                    timeout=3)
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/button_apply').click(timeout=3)
                time.sleep(1)
                self.device(resourceId='com.miui.gallery:id/ok').click(timeout=3)
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/btn_confirm').click(timeout=3)
                time.sleep(2)
                i += 1
        except Exception as e:
            print("定位出错了：", e)

    # 删除预设
    def start_del(self):
        try:
            self.device(text='Smart Aroma Diffuser').click(timeout=3)
            time.sleep(1)
            self.device(resourceId='com.govee.home:id/iv_light_arrow').click(timeout=3)  # 场景编辑
            time.sleep(1)
            while True:
                self.device.xpath('//*[@resource-id="com.govee.home:id/recycle"]/android.view.ViewGroup[3]/android.w'
                                  'idget.ImageView[2]').click(timeout=3)
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/tv_delete').click(timeout=3)
                time.sleep(1)
                self.device(resourceId='com.govee.home:id/btn_done').click(timeout=3)
        except Exception as e:
            print("定位出错了：", e)
        time.sleep(1)


if __name__ == '__main__':
    test = H7161Test()
    test.start_add()
    # test.start_del()
