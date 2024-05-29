#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 2024/4/10 17:39
# @Author  : yansheng.wang
# @File    : test_distribution_network.py
# @Description : 配网压测
import time
import allure
import pytest
import uiautomator2 as u2


from pathlib import Path
from pytest_appautotest.log import get_log


@pytest.fixture
def sku_name():
    sku_info = {
        "sku": "H7148",
        "sku_des": "H7148_34BA"
    }
    return sku_info


@pytest.fixture
def get_success_num():
    success_num = 0
    return success_num


@pytest.fixture()
def get_log_path(sku_name):
    # 脚本日志
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]  # YOLOv5 root directory
    path = str(Path(ROOT) / f"log/{sku_name['sku']}wifi配网压测.txt")
    # serial_path = str(
    #     Path(ROOT) / f"log/{datetime.now().strftime('%Y%m%d_%H%M%S')}{SKU_INFO['sku']}串口log.txt")
    print(path)
    get_logs = get_log.GetLog(path)
    get_logs.info("数据")
    return get_logs


class TestWifi:

    @allure.title("初始化并启动app")
    @allure.description("校验查询购物车所有商品的总数量是否正常")
    def setup_class(self):
        print("初始化：启动app...")
        self.device = u2.connect()
        # self.device = u2.connect('192.168.50.37')
        self.device.app_start('com.govee.home')
        self.device.implicitly_wait(30)  # 元素等待时间30s
        self.width, self.height = self.device.window_size()
        # self.device.settings['operation_delay'] = (1, 1)  # 每次点击后等待2s

    @allure.title("搜索设备")
    def test_search_devices(self, sku_name):
        # self.thread_watch()   # 处理弹窗
        # self.thread_wifi_success_or_fail()  # 串口判断配网是否成功
        """添加设备"""
        # 添加”+“
        if self.device(resourceId="com.govee.home:id/ivDevAdd").exists(timeout=10):
            self.device(resourceId="com.govee.home:id/ivDevAdd").click_exists(timeout=10)
            # 输入要添加的SKU
            self.device(resourceId="com.govee.home:id/tv_search").click_exists(timeout=10)
            self.device(resourceId="com.govee.home:id/et_search").send_keys(sku_name['sku'])
            # 点击SKU
            time.sleep(5)
            while True:
                self.device(resourceId="com.govee.home:id/sku_des").click_exists(timeout=30)
                time.sleep(2)
                if self.device(text="继续").exists():
                    self.device(text="继续").click_exists(timeout=10)
                if self.device(text=sku_name["sku_des"]).exists(timeout=10):
                    assert self.device(text=sku_name["sku_des"]).exists()
                    break
                else:
                    self.device(text='重新扫描').click_exists(timeout=10)

    @allure.title("设备配对")
    def test_select_sku(self, sku_name):
        # 选择设备  H5086_681B   H5086_67c9
        while True:
            self.device(text=sku_name["sku_des"]).click_exists(timeout=10)
            time.sleep(1)
            if self.device(text='配对').exists(timeout=10):
                break
            else:
                if self.device(text="重新连接").exists(timeout=5):
                    self.device(text="重新连接").click_exists(timeout=5)
                if self.device(resourceId='com.govee.home:id/done').exists(timeout=5):
                    break
                print("sku点不到了")
            # 命名设备
            print("点击配对")
        assert self.device(text='配对').exists()

    @allure.title("设备命名")
    def test_click_to_pair(self, sku_name):
        # 继电器模拟点击配对
        if self.device(text='配对').exists(timeout=30):
            time.sleep(2)
            # try:
            #     self.relay_ser.write(bytes.fromhex('A0 01 01 A2'))
            #     time.sleep(0.5)
            #     self.relay_ser.write(bytes.fromhex('A0 01 00 A1'))
            # except Exception as e:
            #     print("继电器串口错误：", e)
        if self.device(resourceId='com.govee.home:id/done').exists(timeout=30):
            while True:
                self.device(resourceId="com.govee.home:id/sensor_name_edit").click_exists(timeout=10)
                self.device(resourceId="com.govee.home:id/sensor_name_edit").send_keys(sku_name["sku"])
                self.device(resourceId="com.govee.home:id/done").click_exists(timeout=10)
                if self.device(text='是').exists(timeout=10):
                    break
        assert self.device(text='是').exists()

    @allure.title("配置网络")
    def test_network(self, sku_name, get_success_num, get_log_path):
        if self.device(text='是').exists(timeout=5):
            self.device(text="是").click_exists(timeout=5)
        # wifi配置
        elif self.device(text='ASUS_F0_2G').exists(timeout=5):
            self.device(resourceId="com.govee.home:id/et_pwd").clear_text()
            self.device(resourceId="com.govee.home:id/et_pwd").send_keys("govee123")
            while True:
                print("配网")
                self.device(resourceId="com.govee.home:id/send_wifi").click_exists(timeout=10)
                if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=60):
                    break
                else:
                    print("配网时出错")
                    # self.error_handle()
        else:
            # 跳过配网
            while True:
                # print("跳过")
                if self.device(resourceId='com.govee.home:id/skip').exists(timeout=10):
                    self.device(resourceId='com.govee.home:id/skip').click_exists(timeout=10)
                    if self.device(resourceId="com.govee.home:id/btn_done").exists(timeout=10):
                        self.device(resourceId="com.govee.home:id/btn_done").click_exists(timeout=10)
                    if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=30):
                        break
                    else:
                        print("跳过时出错")
                        # self.error_handle()
                else:
                    break
        # 绑定完成
        if self.device(resourceId='com.govee.home:id/iv_switch').exists(timeout=30):
            get_success_num += 1
            print(f"配对配网后进入详情页成功次数：{get_success_num}")
            get_log_path.info(f"配对配网后进入详情页成功次数：{get_success_num}")
        assert self.device(resourceId='com.govee.home:id/iv_switch').exists()
        # self.del_device()

    # 删除设备
    @allure.title("删除设备")
    def test_del_device(self, sku_name):
        # 设置
        if self.device(resourceId="com.govee.home:id/ivRightMost").exists(timeout=5):
            # print("删除设备")
            self.device(resourceId="com.govee.home:id/ivRightMost").click_exists(timeout=10)
        elif self.device(resourceId="com.govee.home:id/btn_setting").exists(timeout=5):
            # print("删除设备")
            self.device(resourceId="com.govee.home:id/btn_setting").click_exists(timeout=10)
        time.sleep(2)
        self.down()
        time.sleep(2)
        while True:
            self.down()
            if self.device(text="删除设备").exists(timeout=10):
                self.device(text="删除设备").click_exists(timeout=10)
            # print("删除")
            if self.device(text="是").exists(timeout=10):
                self.device(text="是").click_exists(timeout=10)
                if self.device(resourceId="com.govee.home:id/ivDevAdd").exists(timeout=10):
                    break
            if self.device(text=sku_name["sku"]).exists(timeout=5):
                self.device(text=sku_name["sku"]).click_exists(timeout=5)
                break
            else:
                break
        assert self.device(resourceId="com.govee.home:id/ivDevAdd").exists()

    def down(self):
        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                          0.1 * self.height)  # 向下滑动

    def up(self):
        time.sleep(2)
        self.device.swipe(0.5 * self.width, 0.1 * self.height, 0.5 * self.width,
                          0.9 * self.height)  # 向下滑动
        time.sleep(2)
