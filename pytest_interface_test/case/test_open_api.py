#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 小家电开放API
import json
import random
import time

import allure
import pytest
import requests

DEV_API_KEY = "e3d85d3d-eaa8-4070-b7e3-8ac64b33f9c1"
QA_API_KEY = "d1eb5e56-a8d1-4f10-bf60-59a8c202c973"

# services = "qa"
services = "dev"
sku = "H7137"


@pytest.fixture
def devices_init_info():
    sku_info = {
        "device": None,  # 设备devices
        "sku": None,  # sku
        "sku_type": None,  # 设备功能分类
        "sku_instance": None,  # instance
        "sku_value_enum": None,  # value
        "sku_value_integer": None,  # value
        "type_count": {},
        "services": services,
        "test_sku": sku,
    }
    return sku_info


@pytest.fixture
def get_response(devices_init_info):
    """
    :param devices_init_info:   设备初始化信息
    :return:  返回response
    """
    if devices_init_info["services"] == "qa":  # 正服
        headers = {"Govee-API-Key": QA_API_KEY,
                   "Content-Type": "application/json"}
        response = requests.get(url='https://openapi.api.govee.com/router/api/v1/user/devices',
                                headers=headers)
    else:  # 测服
        headers = {"Govee-API-Key": DEV_API_KEY, "Content-Type": "application/json"}
        response = requests.get(
            url='https://test-openapi.api.govee.com/router/api/v1/user/devices', headers=headers)
    return response


@pytest.fixture
def get_device_or_sku(get_response, devices_init_info):
    """
    :param get_response:
    :param devices_init_info:
    :return: 返回sku和devices
    """
    date = json.loads(get_response.text)
    str_data = json.dumps(date)
    sku_count = str_data.count('sku')
    for i in range(sku_count):  # 遍历sku
        devices_init_info["sku"] = date["data"][i]['sku']  # sku
        # print(devices_init_info["sku"])
        if devices_init_info['sku'] == devices_init_info['test_sku']:
            # print(date[i])
            devices_init_info['device'] = date["data"][i]['device']
        devices_init_info["type_count"] = date["data"][i]['capabilities']
    return devices_init_info["sku"], devices_init_info['device'], devices_init_info["type_count"]


def enum_api(cnname, sku, device, sku_type, instance, value):
    """
    :param cnname:
    :param sku:
    :param device:
    :param sku_type:
    :param instance:
    :param value:
    :return: enum格式数据，开关类：设备开关，夜灯开关、摇头开关
    """
    print("==================执行{0}===================".format(instance))
    try:
        power_json = {
            "requestId": "1",
            "payload": {
                "sku": sku,
                "device": device,
                "capability": {
                    "type": sku_type,
                    "instance": instance,
                    "value": value
                }
            }
        }

        print("send->:", str(power_json).replace("'", '"'))
        if services == "qa":
            headers = {"Govee-API-Key": QA_API_KEY,
                       "Content-Type": "application/json"}
            response = requests.post(url="https://openapi.api.govee.com/router/api/v1/device/control",
                                     headers=headers,
                                     json=power_json)
        else:
            headers = {"Govee-API-Key": DEV_API_KEY,
                       "Content-Type": "application/json"}
            response = requests.post(url="https://test-openapi.api.govee.com/router/api/v1/device/control",
                                     headers=headers,
                                     json=power_json)

        print("receive->", response.text)
        if "200" in str(response):
            if 'failure' in json.loads(response.text)['capability']['state']['status']:
                print(str(cnname) + "：[" + str(value) + "]---->失败")
                print('\n')
            else:
                print(str(cnname) + "：[" + str(value) + "]---->成功")
                print('\n')
            return response.text
        elif "429" in str(response):
            print("Status：429 Too Many Requests")
            return response.text
    except Exception as e:
        print(e)


def auto_mode_api(cnname, sku, device, sku_type, instance, temperature, unit, autoStop=None):
    """
    :param cnname:
    :param sku: H713X  H714X H717X
    :param device:
    :param sku_type:
    :param instance:
    :param temperature:
    :param unit:
    :param autoStop:
    :return: 自动模式、目标温度值、自动停止开关
    """
    print("==================执行{0}===================".format(instance))
    try:
        if autoStop != None:
            mode_json = {
                "requestId": "1",
                "payload": {
                    "sku": sku,
                    "device": device,
                    "capability": {
                        "type": sku_type,
                        "instance": instance,
                        "value": {
                            "temperature": temperature,
                            "unit": unit,
                            "autoStop": autoStop
                        }
                    }
                }
            }
        else:
            mode_json = {
                "requestId": "1",
                "payload": {
                    "sku": sku,
                    "device": device,
                    "capability": {
                        "type": sku_type,
                        "instance": instance,
                        "value": {
                            "temperature": temperature,
                            "unit": unit
                        }
                    }
                }
            }
        print("send->:", str(mode_json).replace("'", '"'))
        if services == "qa":
            headers = {"Govee-API-Key": QA_API_KEY,
                       "Content-Type": "application/json"}
            response = requests.post(url="https://openapi.api.govee.com/router/api/v1/device/control",
                                     headers=headers,
                                     json=mode_json)
        else:
            headers = {"Govee-API-Key": DEV_API_KEY,
                       "Content-Type": "application/json"}
            response = requests.post(url="https://test-openapi.api.govee.com/router/api/v1/device/control",
                                     headers=headers,
                                     json=mode_json)
        print("receive->", response.text)
        if "200" in str(response):
            if 'failure' in json.loads(response.text)['capability']['state']['status']:
                print(str(cnname) + "[温度：" + str(temperature) + "度" + " 自动开关：" + str(
                    autoStop) + " 温度单位：" + str(unit) + "]---->失败")
                print('\n')

            else:
                print(str(cnname) + "[温度：" + str(temperature) + "度" + " 自动开关：" + str(
                    autoStop) + " 温度单位：" + str(unit) + "]---->成功")
                print('\n')
            return response.text
        elif "429" in str(response):
            print("Status：429 Too Many Requests")
            return response.text
    except Exception as e:
        print(e)
        # pass
    time.sleep(5)


def range_auto_mode_api(cnname, sku, device, sku_type, instance, unit, gearMode, lowerSetpoint, upperSetpoint,
                        autoStop=None):
    """

    :param cnname:
    :param sku:
    :param device:
    :param sku_type:
    :param instance:
    :param unit: 单位
    :param gearMode:  档位
    :param lowerSetpoint: 低温度值
    :param upperSetpoint: 高温度值
    :param autoStop:
    :return: 自动模式、范围目标温度值、自动停止开关
    """
    print("==================执行{0}===================".format(instance))
    try:
        if autoStop != None:
            mode_json = {
                "requestId": "1",
                "payload": {
                    "sku": sku,
                    "device": device,
                    "capability": {
                        "type": sku_type,
                        "instance": instance,
                        "value": {
                            "lowerSetpoint": lowerSetpoint,
                            "upperSetpoint": upperSetpoint,
                            "gearMode": gearMode,
                            "unit": unit,
                            "autoStop": autoStop
                        }
                    }
                }
            }
        print("send->:", str(mode_json).replace("'", '"'))
        if services == "qa":
            headers = {"Govee-API-Key": QA_API_KEY,
                       "Content-Type": "application/json"}
            response = requests.post(url="https://openapi.api.govee.com/router/api/v1/device/control",
                                     headers=headers,
                                     json=mode_json)
        else:
            headers = {"Govee-API-Key": DEV_API_KEY,
                       "Content-Type": "application/json"}
            response = requests.post(url="https://test-openapi.api.govee.com/router/api/v1/device/control",
                                     headers=headers,
                                     json=mode_json)
        print("receive->", response.text)
        if "200" in str(response):
            if 'failure' in json.loads(response.text)['capability']['state']['status']:
                print(str(cnname) + "[温度：" + str(lowerSetpoint) + "-" + str(
                    upperSetpoint) + "度" + "档位：" + str(gearMode) + " 自动开关：" + str(
                    autoStop) + " 温度单位：" + str(unit) + "]---->失败")
                print('\n')
            else:
                print(str(cnname) + "[温度：" + str(lowerSetpoint) + "-" + str(
                    upperSetpoint) + "度" + "档位：" + str(gearMode) + " 自动开关：" + str(
                    autoStop) + " 温度单位：" + str(unit) + "]---->成功")
                print('\n')
        elif "429" in str(response):
            print("Status：429 Too Many Requests")
    except Exception as e:
        print(e)
    time.sleep(5)


def work_mode_api(cnname, sku, device, sku_type, instance, workModeValue, modeValue=None):
    """
    :param cnname: 测试功能
    :param sku: ALL
    :param device:
    :param sku_type:
    :param instance:
    :param workModeValue:
    :param modeValue:
    :return:
    """
    print("==================执行{0}===================".format(instance))
    try:
        if modeValue != None:

            work_mode_json = {
                "requestId": "1",
                "payload": {
                    "sku": sku,
                    "device": device,
                    "capability": {
                        "type": sku_type,
                        "instance": instance,
                        "value": {
                            "workMode": workModeValue,
                            "modeValue": modeValue
                        }
                    }
                }
            }
        else:
            work_mode_json = {
                "requestId": "1",
                "payload": {
                    "sku": sku,
                    "device": device,
                    "capability": {
                        "type": sku_type,
                        "instance": instance,
                        "value": {
                            "workMode": workModeValue
                        }
                    }
                }
            }
        print("send->:", str(work_mode_json).replace("'", '"'))
        if services == "qa":
            headers = {"Govee-API-Key": QA_API_KEY,
                       "Content-Type": "application/json"}
            response = requests.post(url="https://openapi.api.govee.com/router/api/v1/device/control",
                                     headers=headers,
                                     json=work_mode_json)
        else:
            headers = {"Govee-API-Key": DEV_API_KEY,
                       "Content-Type": "application/json"}
            response = requests.post(url="https://test-openapi.api.govee.com/router/api/v1/device/control",
                                     headers=headers,
                                     json=work_mode_json)
        print("receive->", response.text)
        if "200" in str(response):
            if 'failure' in json.loads(response.text)['capability']['state']['status']:
                print(str(cnname) + "[模式：" + str(workModeValue) + " 档位：" + str(modeValue) + "]---->失败")
                print('\n')
            else:
                print(str(cnname) + "[模式：" + str(workModeValue) + " 档位：" + str(modeValue) + "]---->成功")
                print('\n')
            return response.text
        elif "429" in str(response):
            print("Status：429 Too Many Requests")
            return response.text
    except Exception as e:
        print(e)
        # pass
    time.sleep(5)


class TestApi:

    @allure.title("开关机")
    @pytest.mark.parametrize("power", [-1, 0, 1, 2])
    def test_power(self, get_device_or_sku, devices_init_info, power):
        sku, device, device_info = get_device_or_sku
        if "powerSwitch" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                if instance == "powerSwitch":
                    cn_name = "设备开关"
                    code = enum_api(cn_name, sku, device, sku_type, instance, power)
                    if "200" in code:
                        assert True
                    elif "400" in code:
                        assert True
                    else:
                        assert False
        time.sleep(5)

    @pytest.mark.skip
    @allure.title("摇头开关")
    @pytest.mark.parametrize("oscillationToggle_power", [-1, 0, 1, 2])
    def test_oscillationToggle_power(self, get_device_or_sku, devices_init_info, oscillationToggle_power):
        sku, device, device_info = get_device_or_sku
        if "oscillationToggle" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                if instance == "oscillationToggle":
                    cn_name = "摇头"
                    code = enum_api(cn_name, sku, device, sku_type, instance, oscillationToggle_power)
                    if "200" in code:
                        assert True
                    elif "400" in code:
                        assert True
                    else:
                        assert False
        time.sleep(5)

    @pytest.mark.skip
    @allure.title("夜灯开关")
    @pytest.mark.parametrize("nightlightToggle_power", [-1, 0, 1, 2])
    def test_nightlightToggle_power(self, get_device_or_sku, devices_init_info, nightlightToggle_power):
        sku, device, device_info = get_device_or_sku
        if "nightlightToggle" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                # 夜灯开关
                if instance == "nightlightToggle":
                    cn_name = "夜灯开关"
                    code = enum_api(cn_name, sku, device, sku_type, instance, nightlightToggle_power)
                    if "200" in code:
                        assert True
                    elif "400" in code:
                        assert True
                    else:
                        assert False
        time.sleep(5)

    @pytest.mark.skip
    @allure.title("摆叶开关")
    @pytest.mark.parametrize("airDeflectorToggle_power", [-1, 0, 1, 2])
    def test_nightlightToggle_power(self, get_device_or_sku, devices_init_info, airDeflectorToggle_power):
        sku, device, device_info = get_device_or_sku
        if "airDeflectorToggle" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                # 摆叶
                if instance == "airDeflectorToggle":
                    cn_name = "摆叶"
                    code = enum_api(cn_name, sku, device, sku_type, instance, airDeflectorToggle_power)
                    if "200" in code:
                        assert True
                    elif "400" in code:
                        assert True
                    else:
                        assert False

    @pytest.mark.skip
    @allure.title("水壶目标温度")
    @pytest.mark.parametrize("temperature,unit",
                             [(random.randint(40, 100), "Celsius"), (39, "Celsius"), (101, "Celsius"),
                              (random.randint(104, 212), "Fahrenheit"), (103, "Fahrenheit"), (213, "Fahrenheit")])
    def test_sliderTemperature(self, get_device_or_sku, devices_init_info, temperature, unit):
        sku, device, device_info = get_device_or_sku
        if "sliderTemperature" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                #     # 目标温度
                if instance == "sliderTemperature":
                    cn_name = "水壶目标温度"
                    auto_mode_api(cn_name, sku, device, sku_type, instance, temperature, unit)

    @pytest.mark.skip
    @allure.title("取暖器目标温度")
    @pytest.mark.parametrize("temperature,unit,auto_value",
                             [(random.randint(5, 30), "Celsius", 1), (random.randint(5, 30), "Celsius", 0),
                              (4, "Celsius", 1), (31, "Celsius", 0),
                              (random.randint(41, 86), "Fahrenheit", 1), (random.randint(41, 86), "Fahrenheit", 0),
                              (40, "Fahrenheit", 1), (87, "Fahrenheit", 0)])
    def test_targetTemperature(self, get_device_or_sku, devices_init_info, temperature, unit, auto_value):
        sku, device, device_info = get_device_or_sku
        if "targetTemperature" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                #     # 目标温度
                if instance == "targetTemperature":
                    cn_name = "目标温度"
                    if "H713" in sku:
                        auto_mode_api(cn_name, sku, device, sku_type, instance,
                                      temperature, unit, auto_value)

    @pytest.mark.skip
    @allure.title("取暖器目标温度范围")
    @pytest.mark.parametrize("unit,gearMode,lower,upper,auto_value",
                             [("Celsius", 1, random.randint(5, 30), random.randint(5, 30), 1),
                              ("Celsius", 2, random.randint(5, 30), random.randint(5, 30), 0),
                              ("Celsius", 3, random.randint(5, 30), random.randint(5, 30), 1),
                              ("Celsius", 3, 4, 31, 0),
                              ("Fahrenheit", 1, random.randint(41, 50), random.randint(60, 86), 1),
                              ("Fahrenheit", 2, random.randint(41, 50), random.randint(60, 86), 0),
                              ("Fahrenheit", 3, random.randint(41, 50), random.randint(60, 86), 1),
                              ("Celsius", 3, 40, 87, 0)])
    def test_targetTemperature(self, get_device_or_sku, devices_init_info, unit, gearMode, lower, upper, auto_value):
        sku, device, device_info = get_device_or_sku
        if "rangeTemperature" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                #     # 目标温度
                if instance == "rangeTemperature":
                    cn_name = "目标温度范围"
                    if "H713" in sku:
                        range_auto_mode_api(cn_name, sku, device, sku_type, instance, unit, gearMode, lower, upper,
                                            auto_value)

    @pytest.mark.skip
    @allure.title("夜灯场景")
    # @pytest.mark.parametrize("nightlightScene_value", [-1, 0, 1, 2])
    def test_nightlightScene(self, get_device_or_sku, devices_init_info, ):
        sku, device, device_info = get_device_or_sku
        if "nightlightToggle" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                # 夜灯场景
                if instance == "nightlightScene":
                    cn_name = "夜灯场景"
                    self.sku_value_enum = mode_type['parameters']['options']
                    for i in self.sku_value_enum:
                        value = i['value']
                        enum_api(cn_name, sku, device, sku_type, instance, value)

    @pytest.mark.skip
    @allure.title("夜灯亮度")
    # @pytest.mark.skipif(not is_brightness_condition_met(), reason="没有夜灯亮度")
    @pytest.mark.parametrize("brightness_value", [random.randint(1, 100), random.randint(1, 100)])
    def test_nightlightScene(self, get_device_or_sku, devices_init_info, brightness_value):
        sku, device, device_info = get_device_or_sku
        if "brightness" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                cn_name = "夜灯亮度"
                sku_type = mode_type['type']
                instance = mode_type['instance']
                # 夜灯亮度
                if instance == "brightness":
                    print("夜灯亮度:", brightness_value)
                    enum_api(cn_name, sku, device, sku_type, instance, brightness_value)

    @pytest.mark.skip
    @allure.title("夜灯颜色")
    # @pytest.mark.skipif(not is_colorRgb_condition_met(), reason="没有夜灯颜色")
    @pytest.mark.parametrize("colorRgb_value",
                             [16711680, 65280, 255, 1, random.randint(1, 16777215), 16777215, 16777216])
    def test_colorRgb(self, get_device_or_sku, devices_init_info, colorRgb_value):
        sku, device, device_info = get_device_or_sku
        if "colorRgb" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                cn_name = "夜灯亮度"
                sku_type = mode_type['type']
                instance = mode_type['instance']
                # 夜灯颜色
                if instance == "colorRgb":
                    # result = (255 << 16) + (255 << 8) + 255  # 颜色算法
                    print("夜灯颜色:", colorRgb_value)
                    enum_api(cn_name, sku, device, sku_type, instance, colorRgb_value)

    @pytest.mark.skip
    @allure.title("目标湿度")
    # @pytest.mark.skipif(not is_humidity_condition_met(), reason="没有夜灯颜色")
    @pytest.mark.parametrize("humidity_value",
                             [random.randint(30, 80), random.randint(30, 80)])
    def test_humidity(self, get_device_or_sku, devices_init_info, humidity_value):
        sku, device, device_info = get_device_or_sku
        if "humidity" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                # 目标湿度
                if instance == "humidity":
                    cn_name = "目标湿度"
                    enum_api(cn_name, sku, device, sku_type, instance, humidity_value)

    @allure.title("模式档位")
    @pytest.mark.parametrize("H713x_workMode_value,H713x_workGear_value",
                             ([(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (9, 0), (3, 0)]))
    def test_workMode_H713X(self, get_device_or_sku, devices_init_info,
                            H713x_workMode_value, H713x_workGear_value):
        sku, device, device_info = get_device_or_sku
        if "workMode" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if sku in ["H713A", "H7130"]:
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                # 摆叶
                if instance == "workMode":
                    cn_name = "模式/档位"
                    # api.enum_api(sku, device, sku_type, instance, 0, "设备关机")  # 设备关机
                    work_mode_api(cn_name, sku, device, sku_type, instance,
                                  H713x_workMode_value, H713x_workGear_value)

    @pytest.mark.skip
    @allure.title("模式档位")
    @pytest.mark.parametrize("H7130_workMode_value", ([0, 1, 2, 3, 4]))
    def test_workMode_H7130(self, get_device_or_sku, devices_init_info, H7130_workMode_value):
        sku, device, device_info = get_device_or_sku
        if "workMode" not in str(device_info):
            pytest.skip("没有该功能，跳过测试用例")
        if sku not in ["H713A", "H713A"]:
            pytest.skip("没有该功能，跳过测试用例")
        if devices_init_info["test_sku"] == devices_init_info["sku"]:  # 指定sku测试
            print("sku--->", sku)
            print("Device--->", device)
            for mode_type in device_info:  # 遍历每个sku里的所有模式
                # print(mode_type)
                sku_type = mode_type['type']
                instance = mode_type['instance']
                # 摆叶
                if instance == "workMode":
                    cn_name = "模式/档位"
                    # api.enum_api(sku, device, sku_type, instance, 0, "设备关机")  # 设备关机
                    work_mode_api(cn_name, sku, device, sku_type, instance,
                                  H7130_workMode_value)

    #     # 模式，档位
    #     elif instance == "workMode":
    #         cn_name = "模式/档位"
    #         # api.enum_api(sku, device, sku_type, instance, 0, "设备关机")  # 设备关机
    #         if "H713" in sku:
    #             if sku == "H713A" or sku == "H7130":
    #                 mode_list = [0, 1, 2, 3, 4]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode)
    #             else:
    #                 mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (9, 0), (3, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #         elif "H714" in sku:
    #             mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
    #                          (1, 10), (2, 0),
    #                          (3, 0)]
    #             for mode in mode_list:
    #                 self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                    mode[0],
    #                                    mode[1])
    #         elif "H716" in sku:
    #             mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
    #                          (1, 10), (2, 0), (3, 0)]
    #             for mode in mode_list:
    #                 self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                    mode[0],
    #                                    mode[1])
    #         elif "H717" in sku:
    #             if sku in ["H7170", "H7175"]:
    #                 mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0), (3, 0), (4, 0),
    #                              (5, 0), (6, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             elif sku == "H7173":
    #                 mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0), (2, 1), (3, 0),
    #                              (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 0), (4, 1), (4, 2), (4, 3),
    #                              (4, 4), (4, 5)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             elif sku in ["H7171", "H717A"]:
    #                 mode_list = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             elif sku == "H7172":  # 制冰机
    #                 mode_list = [(1, 0), (2, 0), (3, 0), (4, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             else:
    #                 mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0), (2, 1), (3, 0),
    #                              (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 0), (4, 1), (4, 2), (4, 3),
    #                              (4, 4), (4, 5)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #         elif "H718" in sku:  # 厨余机
    #             mode_list = [(1, 0), (2, 0), (3, 0), (0, 0), (4, 0)]
    #             for mode in mode_list:
    #                 self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                    mode[0],
    #                                    mode[1])
    #         elif "H712" in sku:
    #             if sku == "H7120":
    #                 mode_list = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (5, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             elif sku == "H7126":
    #                 mode_list = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (3, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             elif sku == "H7121":
    #                 mode_list = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (16, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             elif sku == "H7123":
    #                 mode_list = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (3, 0), (5, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             elif sku == "H7122":
    #                 mode_list = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2),
    #                              (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11),
    #                              (2, 12), (2, 13), (2, 14), (3, 0), (3, 1), (5, 0), (5, 1)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             else:
    #                 mode_list = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2),
    #                              (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11),
    #                              (2, 12), (2, 13), (2, 14), (3, 0), (3, 1), (5, 0), (5, 1)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #         elif "H715" in sku:
    #             mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (3, 0), (8, 0), (1, 1)]
    #             for mode in mode_list:
    #                 self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                    mode[0],
    #                                    mode[1])
    #         elif "H710" or "H711" in sku:
    #             if sku == "H7112":
    #                 mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
    #                              (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
    #                              (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
    #                              (5, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #             else:
    #                 mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
    #                              (2, 0), (3, 0),
    #                              (5, 0), (6, 0), (7, 0)]
    #                 for mode in mode_list:
    #                     self.work_mode_api(sku, device, sku_type, instance, cn_name,
    #                                        mode[0],
    #                                        mode[1])
    #

    #     # 加湿器 热雾
    #     elif instance == "hotFogToggle":
    #         cn_name = "热雾"
    #         hotFogToggle = (1, 0)
    #         for value_on in hotFogToggle:
    #             api.enum_api(sku, device, sku_type, instance, value_on, cn_name)

    #     elif instance == "lightScene":
    #         if sku == 'H7161':
    #             for value in [12549, 12550, 12551, 12552, 12553, 12554, 12555, 12556, 12557, 12558, 12559, 12560,
    #                           12561, 12562]:
    #                 print("夜灯颜色:", value)
    #                 api.enum_api(sku, device, sku_type, instance, value)
    #         elif sku == 'H7162':
    #             for value in [12631, 12632, 12633, 12634, 12635, 12636, 12637, 12638, 12639, 12640,
    #                           12641, 12642, 12643, 12644]:
    #                 print("夜灯颜色:", value)
    #                 api.enum_api(sku, device, sku_type, instance, value)
    #     # 除湿机满水事件
    #     elif instance == "waterFullEvent":
    #         cn_name = "除湿机满水事件"
    #         api.enum_api(sku, device, sku_type, instance, 1, cn_name)
    # print("\n")

    #

    #

    #
    # # 状态查询
    # def status_query(self, sku, device):
    #     """
    #     :param sku:
    #     :param device:
    #     :return:    查询状态
    #     """
    #     status_json = {
    #         "requestId": "1",
    #         "payload": {
    #             "sku": sku,
    #             "device": device,
    #         }
    #     }
    #     print("send->:", str(status_json).replace("'", '"'))
    #     if self.services == "qa":
    #         response = requests.post(url="https://openapi.api.govee.com/router/api/v1/device/state",  # 正服
    #                                  headers=self.headers,
    #                                  json=status_json)
    #     else:
    #         response = requests.post(url="https://test-openapi.api.govee.com/router/api/v1/device/state",  # 测服
    #                                  headers=self.headers,
    #                                  json=status_json)
    #     print("receive->", response.text)
    ##     if "200" in str(response):
    #  #       print("receive->", json.loads(response.text)["capabilities"])
