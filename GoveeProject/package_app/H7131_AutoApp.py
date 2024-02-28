import datetime
import threading
import time
import serial

from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction


class ExecuteApp(object):

    def __init__(self, desired_caps):
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
        self.driver.implicitly_wait(30)

    # 添加设备
    def add_devices(self):
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

    # 删除设备
    def del_device(self):
        # 点击设备设置按钮
        TouchAction(self.driver).press(x=1000, y=150).release().perform()  # 通过定位坐标
        time.sleep(2)
        self.swipe_down()  # 下滑
        self.driver.find_element(By.ID, "btn_delete").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "btn_done").click()
        time.sleep(5)

    # app主页
    def app_home(self):
        # 进入设备详情页
        try:
            self.driver.find_element(By.ID, "rl_item").click()
            time.sleep(5)
        except Exception:
            print("定位出错")

    # 控制设备详情页头部上半部分功能
    def auto_app_top(self):
        try:
            # 点击开关
            self.driver.find_element(By.ID, "iv_switch").click()
            time.sleep(2)
            self.driver.find_element(By.ID, "iv_switch").click()
            time.sleep(2)
            # 低挡
            self.driver.find_element(By.ID, "iv_gear_low_bg").click()
            time.sleep(2)
            # 中挡
            self.driver.find_element(By.ID, "iv_gear_mid_bg").click()
            time.sleep(2)
            # 高档
            self.driver.find_element(By.ID, "iv_gear_high_icon").click()
            time.sleep(2)
            # 自动挡
            self.driver.find_element(By.ID, "iv_auto_icon").click()
            time.sleep(2)
            # 风扇挡
            self.driver.find_element(By.ID, "iv_fan_icon").click()
            time.sleep(2)
        except Exception:
            print("定位出错")

    # 控制设备详情页头部下半部分功能
    def auto_app_down(self):
        try:
            # 摇头
            self.driver.find_element(By.ID, 'iv_shake_switch').click()
            time.sleep(2)
            # 夜灯
            self.driver.find_element(By.ID, 'iv_light_rgb_switch_ext1').click()
            time.sleep(2)
            # # 锁
            # self.driver.find_element(By.ID, 'iv_lock_switch').click()
            # time.sleep(2)
            # # 显示
            # self.driver.find_element(By.ID, 'iv_light_indicator_switch').click()
            # time.sleep(2)
            # 绑定温湿度计
            # self.driver.find_element(By.ID, 'bind_tempe_container').click()
            # time.sleep(2)
            # self.driver.find_element(By.XPATH, "	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android"
            #                                    ".widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
            #                                    "android.widget.RelativeLayout/android.widget.RelativeLayout/androidx.recyc"
            #                                    "lerview.widget.RecyclerView/android.widget.RelativeLayout[2]").click()
            # time.sleep(2)
            #
            # self.driver.find_element(By.ID, 'btn_ok').click()
            # time.sleep(2)
            # self.driver.find_element(By.ID,"btn_ok").click()  # 定位该id会导致手机界面下拉设置框
            # time.sleep(2)
            # TouchAction(self.driver).press(x=1320, y=230).release().perform()  # 无法通过id定位就通过定位坐标
            # time.sleep(2)
        except Exception:
            print("定位出错")

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


if __name__ == "__main__":
    print("555")
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
    n = 0
    run = ExecuteApp(desired_caps)
    run.app_home()  # 进入设备详情页（）
    while True:
        # run.add_devices()  # 配网

        run.auto_app_top()  # 控制头部功能
        # run.swipe_down()  # 向下滑动
        run.auto_app_down()  # 控制底部功能
        # run.del_device()
        n += 1
        print("测试次数：", n)
