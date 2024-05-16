from loguru import logger
import uiautomator2 as u2
import time
import datetime

d = u2.connect('')
now = datetime.datetime.now()
logger.add("wlan_pick.py.log", rotation="500MB")


def find_tag(element, timeout=5):
    element_to_find = element
    screen_width, screen_height = d.window_size()
    start_time = time.time()

    while not element_to_find.exists:
        if time.time() - start_time > timeout:
            break
        d.swipe(screen_width * 0.5, screen_height * 0.8, screen_width * 0.5, screen_height * 0.2)


def goto_device_settings():
    if d(resourceId="com.govee.home:id/iv_setting").exists(timeout=5):
        logger.info("休眠5S后进入设备设置页面")
        time.sleep(5)
        d(resourceId="com.govee.home:id/iv_setting").click()
    time.sleep(2)
    if not d(resourceId="com.govee.home:id/device_info_label"):
        logger.info("进入设备设置页面,try")
        d(resourceId="com.govee.home:id/tv4OpLabel", text="Wi-Fi设置").click()
    else:
        time.sleep(1)


def goto_wlan_settings():
    logger.info("进入WiFi设置页面")
    if d(resourceId="com.govee.home:id/wifi_setting_container").exists(timeout=5):
        d(resourceId="com.govee.home:id/wifi_setting_container").click()
    time.sleep(2)
    while True:
        if d(resourceId="com.govee.home:id/wifi_searching"):
            logger.info("WiFi搜索中")
            time.sleep(1)
        elif not d(resourceId="com.govee.home:id/aws_title").exists(timeout=5):
            logger.warning("没有进入WiFi设置页面，尝试再次点击")
            d(resourceId="com.govee.home:id/tv4OpLabel", text="Wi-Fi设置").click()
            time.sleep(1)
        if d(resourceId="com.govee.home:id/ble_disconnect_wifi_set_done"):
            logger.info("刷新BLE链接")
            d(resourceId="com.govee.home:id/ble_disconnect_wifi_set_done").click()
            time.sleep(1)
        else:
            break


def wait_wlan_page():
    d(resourceId="com.govee.home:id/wifi_searching").wait_gone() or d(
        resourceId="com.govee.home:id/wifi_choose").wait_gone()
    wait_time = 0
    while wait_time < 18:
        if d(resourceId="com.govee.home:id/other_wifi_name").exists(timeout=5):
            logger.info("直接输入账号密码")
            break
        # if d(resourceId="com.govee.home:id/ble_disconnect_wifi_set_done").exists(timeout=5):
        #     logger.warning("WiFi列表加载异常，刷新")
        #     d(resourceId="com.govee.home:id/ble_disconnect_wifi_set_done").click()
        #     d(resourceId="com.govee.home:id/wifi_arrow").click()
        #     find_tag(d(resourceId="com.govee.home:id/wifi_name", text="其他…"))
        #     logger.info("点击其他，进入手动输入")
        #     d(resourceId="com.govee.home:id/wifi_name", text="其他…").click()
        #     break
        if d(resourceId="com.govee.home:id/wifi_hint").exists(timeout=5):
            logger.warning("获取Wi-Fi列表失败，可直接输入SSID和密码")
            break
        if not d(resourceId="com.govee.home:id/other_wifi_name").exists(timeout=5):
            logger.info("点击打开WiFi列表")
            d(resourceId="com.govee.home:id/wifi_arrow").click()
            logger.info("滑动列表")
            find_tag(d(resourceId="com.govee.home:id/wifi_name", text="其他…"))
            logger.info("点击其他，进入手动输入")
            d(resourceId="com.govee.home:id/wifi_name", text="其他…").click()
        if not d(resourceId="com.govee.home:id/send_wifi").exists(timeout=5):
            logger.info("没有进入WiFi页面，尝试再次点击")
            d.xpath('//*[@text="其他…"]').click()
            break
        wait_time += 1


def send_name_pwd(ssid, pwd):
    global defeat_sum_1, defeat_sum_2, connect_time
    logger.info("输入SSID和密码")
    d(resourceId="com.govee.home:id/other_wifi_name").send_keys(ssid)
    d(resourceId="com.govee.home:id/et_pwd").send_keys(pwd)
    time.sleep(1)
    logger.info("点击收起键盘")
    d.press("back")
    time.sleep(1)
    d(resourceId="com.govee.home:id/send_wifi").click()
    logger.info("开始配网")
    start_time = time.time()
    time.sleep(0.5)
    while True:
        if d(resourceId="com.govee.home:id/send_wifi").exists:
            nowtime = datetime.datetime.now()
            d.screenshot(
                '{}.png'.format("../log/screen/" + devices + ssid + "_wlan_pick" + nowtime.strftime("%Y-%m-%d_%H-%M")))

            if ssid == ssid_1:
                defeat_sum_1 += 1
                logger.warning(ssid + "失败{}次".format(defeat_sum_1))
            else:
                defeat_sum_2 += 1
                logger.warning(ssid + "失败{}次".format(defeat_sum_2))
            raise Exception(ssid + "联网失败")
        if d(resourceId="com.govee.home:id/bg4Name") or d(resourceId="com.govee.home:id/device_name_container"):
            break
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(ssid + "联网耗时: {:.2f}s".format(elapsed_time))
    return elapsed_time


def check_list():
    if d(resourceId="com.govee.home:id/btn_switch").exists(timeout=5):
        logger.info("在设备详情页，准备进入设置页面 ")
    else:
        logger.info("进入设备详情页面")

        if d(resourceId="com.govee.home:id/tvName", text=devices).exists(timeout=30):
            d(resourceId="com.govee.home:id/tvName", text=devices).click()
        time.sleep(3)
        if d(resourceId="com.govee.home:id/tvName", text=devices).exists(timeout=30):
            d(resourceId="com.govee.home:id/tvName", text=devices).click()
        if d(resourceId="com.govee.home:id/btn_done").exists(timeout=30):
            d(resourceId="com.govee.home:id/btn_done").click()
        time.sleep(3)
        if d(resourceId="com.govee.home:id/btn_done").exists(timeout=30):
            d(resourceId="com.govee.home:id/btn_done").click()


if __name__ == '__main__':
    defeat_sum_1 = 0
    defeat_sum_2 = 0
    connect_time_1 = 0
    connect_time_2 = 0
    main_cout = 0
    count_1 = 0
    count_2 = 0
    total_time_1 = 0
    total_time_2 = 0
    max_time_1 = 0
    min_time_1 = float('inf')
    max_time_2 = 0
    min_time_2 = float('inf')
    devices = "F54A"
    ssid_1 = "DIR-882"
    pwd_1 = "20170201"
    ssid_2 = "ASUS_AX3000_2.4G"
    pwd_2 = "20170201a"
    logger.add("../log/" + devices + "_wlan_H600D" + now.strftime("%Y-%m-%d_%H-%M") + ".log", rotation="50MB")
    while True:
        try:
            goto_device_settings()
            goto_wlan_settings()
            wait_wlan_page()

            elapsed_time_1 = send_name_pwd(ssid_1, pwd_1)
            if elapsed_time_1 > 20:
                connect_time_1 += 1
            count_1 += 1
            logger.info(ssid_1 + "成功{}次".format(count_1))

            total_time_1 += elapsed_time_1
            max_time_1 = max(max_time_1, elapsed_time_1)
            min_time_1 = min(min_time_1, elapsed_time_1)

            time.sleep(10)

            # goto_device_settings()
            goto_wlan_settings()
            wait_wlan_page()

            elapsed_time_2 = send_name_pwd(ssid_2, pwd_2)
            if elapsed_time_2 > 20:
                connect_time_2 += 1
            count_2 += 1
            logger.info(ssid_2 + "成功{}次".format(count_2))

            total_time_2 += elapsed_time_2
            max_time_2 = max(max_time_2, elapsed_time_2)
            min_time_2 = min(min_time_2, elapsed_time_2)
            main_cout += 1
            # logger.info("配网流程已运行了{:.2f}次".format(main_cout))

            avg_time_1 = total_time_1 / (count_1)
            avg_time_2 = total_time_2 / (count_2)
            logger.info(
                "{}第{}次配网测试，成功{}次，失败{}次,平均时间：{:.2f}s,最小时间: {:.2f}s,最大时间: {:.2f}s,大于20秒的{}次".format(
                    ssid_1, (count_1 + defeat_sum_1), count_1, defeat_sum_1, avg_time_1, min_time_1, max_time_1, connect_time_1))
            logger.info(
                "{}第{}次配网测试，成功{}次，失败{}次,平均时间：{:.2f}s,最小时间: {:.2f}s,最大时间: {:.2f}s,大于20秒的{}次".format(
                    ssid_2, (count_2 + defeat_sum_2),count_2 , defeat_sum_2, avg_time_2, min_time_2, max_time_2, connect_time_2))
        except Exception as e:
            logger.warning("出现异常，重启APP")
            d.app_stop("com.govee.home")
            d.app_start("com.govee.home")
            check_list()
