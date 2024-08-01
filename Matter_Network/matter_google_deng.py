import datetime
import random
import time

import serial
import uiautomator2 as u2
from loguru import logger

d = u2.connect()
d.implicitly_wait(30)  # 元素等待时间30s
# d.settings['operation_delay'] = (0, 2)  # 每次点击后等待2s
now = datetime.datetime.now()
logger.add("./log/" + 'H6011_matter' + now.strftime("%Y-%m-%d_%H-%M") + ".log", rotation="50MB")


def re_factory():
    logger.info('开始恢复出厂')
    # switch = serial.Serial('com4', 9600)
    # outage = serial.Serial('com55', 9600)
    music = serial.Serial('com17', 9600)
    d = bytes.fromhex('A0 01 01 A2')
    e = bytes.fromhex('A0 01 00 A1')
    # music.write(d)
    time.sleep(0.2)
    i = 0
    while i < 4:
        music.write(d)
        time.sleep(1)
        music.write(e)
        time.sleep(3)
        i += 1
        # print(i)
    music.write(d)
    # switch.write(e)
    logger.info('恢复出厂后等待30秒')
    time.sleep(30)
    # outage.write(e)
    # time.sleep(5)
    # outage.write(d)
    # switch.close()
    music.close()
    # outage.close()


def re_app():
    # print(d.info)
    logger.warning("出现异常，重启APP")
    d.app_stop("com.google.android.apps.chromecast.app")
    d.app_stop("com.google.android.gms")
    logger.info('stop app')
    time.sleep(1)
    d.app_start("com.google.android.apps.chromecast.app", use_monkey=True)
    logger.info('start app')
    time.sleep(5)
    d(resourceId="com.google.android.apps.chromecast.app:id/bottom_navigation_bar_devices_item").click(timeout=10)
    logger.info('点击设备栏')
    re_factory()
    d(scrollable=True).scroll.vert.backward()
    d.xpath(
        '//*[@resource-id="com.google.android.apps.chromecast.app:id/home_view_refresh_layout"]/android.widget.ImageView[1]').wait_gone(
        90)
    if d(resourceId="com.google.android.apps.chromecast.app:id/title", text="111").exists(timeout=3):
        delete()


def make():
    global code
    d.app_start("com.google.android.apps.chromecast.app", use_monkey=True)
    if d(resourceId="com.google.android.apps.chromecast.app:id/bottom_navigation_bar_devices_item").exists(timeout=3):
        d(resourceId="com.google.android.apps.chromecast.app:id/bottom_navigation_bar_devices_item").click(timeout=5)
        logger.info('点击设备')

    if d(resourceId="com.google.android.apps.chromecast.app:id/add_devices_fab").exists(timeout=3):
        d(resourceId="com.google.android.apps.chromecast.app:id/add_devices_fab").click(timeout=5)
        logger.info('点击添加')

    if d(resourceId="com.google.android.apps.chromecast.app:id/line1", text="支持 Matter 的设备").exists(timeout=3):
        d(resourceId="com.google.android.apps.chromecast.app:id/line1", text="支持 Matter 的设备").click(timeout=5)
        logger.info('支持 Matter 的设备')
    time.sleep(2)

    if d(resourceId="com.google.android.gms.optional_home:id/qr_icon").exists(timeout=3):
        d.xpath(
            '//*[@resource-id="com.google.android.gms.optional_home:id/cutoutLayout"]/android.view.ViewGroup[1]').click(
            timeout=5)
        logger.info('选择手动输入matter配对码')

    if d(resourceId="com.google.android.gms.optional_home:id/titleText").exists(timeout=3):
        d(resourceId="com.google.android.gms.optional_home:id/setupCodeLayout").click(timeout=5)
        d.xpath(
            '//*[@resource-id="com.google.android.gms.optional_home:id/setupCodeLayout"]/android.widget.FrameLayout[1]').click(
            timeout=5)
        d.send_keys(code)
        logger.info('输入matter配对码')

    # if d(resourceId="com.android.systemui:id/back").exists(timeout=3):
    #     d(resourceId="com.android.systemui:id/back").click(timeout=5)

    if d(resourceId="com.google.android.gms.optional_home:id/nextButton").exists(timeout=3):
        d(resourceId="com.google.android.gms.optional_home:id/nextButton").click(timeout=5)
        logger.info('点击下一步')

    if d(resourceId="com.google.android.gms.optional_home:id/confirmButton").exists(timeout=3):
        d(resourceId="com.google.android.gms.optional_home:id/confirmButton").click(timeout=5)
        logger.info('点击同意')

    if d(resourceId="com.google.android.gms.optional_home:id/common_exit").exists(timeout=3):
        d(resourceId="com.google.android.gms.optional_home:id/common_exit").click(timeout=5)
        logger.info('连接失败,找不到设备')
        raise Exception('连接失败,找不到设备')
    time.sleep(random.randint(1, 10))
    if d(text="仍然设置").exists(timeout=180):
        d.click(0.157, 0.925)
        logger.info('点击仍然设置')
    start_time = time.time()
    time.sleep(0.5)
    while True:
        if d(resourceId="com.google.android.gms.optional_home:id/header_title").exists():
            break
        if d(resourceId="com.google.android.gms.optional_home:id/title").exists():
            nowtime = datetime.datetime.now()
            d.screenshot(
                '{}.png'.format("./screen/" + "_wlan_pick" + nowtime.strftime("%Y-%m-%d_%H-%M-%S")))
            raise Exception("联网失败")

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info("联网耗时: {:.2f}s".format(elapsed_time))

    if d(resourceId="com.google.android.gms.optional_home:id/header_title").exists(timeout=3):
        logger.info('连接成功')
        d(resourceId="com.google.android.gms.optional_home:id/positive_button").click(timeout=5)
        logger.info('点击完成')

    if d(resourceId="com.google.android.apps.chromecast.app:id/title_text").exists(timeout=3):
        logger.info('选择房间')
        d.xpath(
            '//*[@resource-id="com.google.android.apps.chromecast.app:id/recycler_view"]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]').click(
            timeout=5)

    if d(resourceId="com.google.android.apps.chromecast.app:id/primary_button").exists(timeout=3):
        d(resourceId="com.google.android.apps.chromecast.app:id/primary_button").click(timeout=5)
        logger.info('点击下一步')

    if d(resourceId="com.google.android.apps.chromecast.app:id/primary_button").exists(timeout=3):
        d(resourceId="com.google.android.apps.chromecast.app:id/primary_button").click(timeout=5)
        logger.info('点击下一步')

    if d(resourceId="com.google.android.apps.chromecast.app:id/toolbar_container").exists(timeout=120):
        d(scrollable=True).scroll.vert.backward()
        d.xpath(
            '//*[@resource-id="com.google.android.apps.chromecast.app:id/home_view_refresh_layout"]/android.widget.ImageView[1]').wait_gone(
            120)
        logger.info('进入设备列表')
    return elapsed_time


def delete():
    logger.info('开始删除设备')
    if d(resourceId="com.google.android.apps.chromecast.app:id/title", text="111").exists(timeout=3):
        d(resourceId="com.google.android.apps.chromecast.app:id/title", text="111").long_click(3)
        logger.info('长按3秒进入设备详情页')
    if d(resourceId="com.google.android.apps.chromecast.app:id/title", text="yinxiang 2").exists():
        d(resourceId="com.google.android.apps.chromecast.app:id/title", text="yinxiang 2").long_click(3)
        logger.info('长按3秒进入设备详情页')
    if d(resourceId="com.google.android.apps.chromecast.app:id/title", text="yinxiang的灯").exists():
        d(resourceId="com.google.android.apps.chromecast.app:id/title", text="yinxiang的灯").long_click(3)
        logger.info('长按3秒进入设备详情页')
    time.sleep(3)
    if d(resourceId="com.google.android.apps.chromecast.app:id/settings_button").exists(timeout=10):
        d(resourceId="com.google.android.apps.chromecast.app:id/settings_button").click(timeout=3)
        logger.info('点击设置')
    if d(resourceId="com.google.android.apps.chromecast.app:id/TextView_title", text="移除设备").exists(timeout=30):
        d(resourceId="com.google.android.apps.chromecast.app:id/TextView_title", text="移除设备").click(timeout=30)
        logger.info('点击移除设备')
        time.sleep(2)
    if d(resourceId="com.google.android.gms.optional_home:id/progress_indicator").wait_gone(120):
        d(resourceId="com.google.android.gms.optional_home:id/remove_button").click(timeout=120)

    if d(resourceId="com.google.android.gms.optional_home:id/remove_button").exists(timeout=120):
        d(resourceId="com.google.android.gms.optional_home:id/remove_button").click(timeout=2)
        logger.info('点击解除关联')

    if d(resourceId='com.google.android.apps.chromecast.app:id/settings_button').exists(timeout=120):
        while True:
            d.xpath('//*[@content-desc="关闭屏幕。"]').click_exists(timeout=5)
            if d(resourceId='com.google.android.apps.chromecast.app:id/top_app_bar_centered_title').exists(timeout=5):
                logger.info('关闭设备页面(删除后google未同步刷新)')
                break
    # else:
    #     raise Exception("loading一直无法加载完成")

    if d(resourceId="com.google.android.apps.chromecast.app:id/toolbar_container").exists(timeout=120):  # 如果回到设备页
        d(scrollable=True).scroll.vert.backward()
        d.xpath(
            '//*[@resource-id="com.google.android.apps.chromecast.app:id/home_view_refresh_layout"]/android.widget.ImageView[1]').wait_gone(
            60)
        logger.info('进入设备列表')


def check_list():
    d.app_start("com.google.android.apps.chromecast.app", use_monkey=True)

    if d(resourceId="com.google.android.apps.chromecast.app:id/bottom_navigation_bar_devices_item").exists(timeout=3):
        d(resourceId="com.google.android.apps.chromecast.app:id/bottom_navigation_bar_devices_item").click(timeout=5)
    # if not d(resourceId="com.google.android.apps.chromecast.app:id/control", description="yinxiang, 音箱."):
    #     re_app()
    if d(resourceId="com.google.android.apps.chromecast.app:id/title", text="111").exists(3):
        delete()
    # if d(resourceId="com.google.android.apps.chromecast.app:id/title", text="yinxiang 2").exists(3):
    #     delete()
    # if d(resourceId="com.google.android.apps.chromecast.app:id/title", text="yinxiang的灯").exists(timeout=3):
    #     delete()


def calculate():
    global count, connect_time, total_time, max_time, min_time
    elapsed_time = make()
    logger.info('开始计算')
    if elapsed_time > 20:
        connect_time += 1
    count += 1
    logger.info("成功{}次".format(count))

    total_time += elapsed_time
    max_time = max(max_time, elapsed_time)
    min_time = min(min_time, elapsed_time)
    avg_time = total_time / count
    logger.info('第{}次配网，成功{}次，平均耗时{:.2f}，最大耗时{:.2f}，最小耗时{:.2f}'.format(count, connect_time, avg_time,
                                                                                          max_time, min_time))


if __name__ == '__main__':
    code = "15766223437"
    connect_time = 0
    count = 0
    total_time = 0
    max_time = 0
    min_time = float('inf')
    while True:
        try:
            check_list()
            re_factory()
            calculate()
            delete()
        except Exception as e:
            print(e)
            re_app()
