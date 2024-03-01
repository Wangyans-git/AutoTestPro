#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 小家电开放API
import json
import time

import random
import requests


class ApiTest:
    def __init__(self,services,sku=None):
        self.device = None  # 设备devices
        self.sku = None  # sku
        self.sku_type = None  # 设备功能分类
        self.sku_instance = None  # instance
        self.sku_value_enum = None  # value
        self.sku_value_integer = None  # value
        self.services = services
        self.test_sku = sku
        if self.services =="qa":  # 正服
            self.headers = {"Govee-API-Key": "d1eb5e56-a8d1-4f10-bf60-59a8c202c973",
                            "Content-Type": "application/json"}
            self.response = requests.get(url='https://openapi.api.govee.com/router/api/v1/user/devices', headers=self.headers)
        else:  # 测服
            self.headers = {"Govee-API-Key": "e3d85d3d-eaa8-4070-b7e3-8ac64b33f9c1", "Content-Type": "application/json"}
            self.response = requests.get(
                url='https://test-openapi.api.govee.com/router/api/v1/user/devices', headers=self.headers)


    # 查询设备
    def all_device(self):
        # print(self.response.text)
        self.date = json.loads(self.response.text)
        # print(date)
        str_data = json.dumps(self.date)
        sku_count = str_data.count('sku')
        for i in range(sku_count):  # 遍历sku
            self.sku = self.date[i]['sku']  # sku
            if self.sku ==self.test_sku:  # 指定sku测试
            # if self.sku in  ["H5160","H5161","H5080","H5081","H5082"]:  # 指定sku测试
            # if 1 == 1:  # 所有sku测试
                print("=========================================")
                print("==================查询===================")
                print("=========================================")
                print("sku--->", self.sku)
                self.device = self.date[i]['device']  # 设备devices
                print("Device--->", self.device)
                api.status_query(self.sku,self.device)   # 查询
                # self.function_device(i)    # 功能
            elif self.test_sku == None:   # 全部测试
                print("=========================================")
                print("==================查询===================")
                print("=========================================")
                print("sku--->", self.sku)
                self.device = self.date[i]['device']  # 设备devices
                print("Device--->", self.device)
                api.status_query(self.sku,self.device)   # 查询
                # self.function_device(i)  # 功能

    def function_device(self,sku):
        type_count = self.date[sku]['capabilities']  # 每个sku中type个数   7173为例：开关、滑块、模式。3种type
        # mode
        print("开始测试{}".format(self.sku))
        # print(type_count)
        for mode_type in type_count:  # 遍历每个sku里的所有模式
            # print(mode_type)
            print("********************************")
            self.sku_type = mode_type['type']
            print(self.sku_type)
            self.sku_instance = mode_type['instance']
            print(self.sku_instance)
            print("********************************")

            """ENUM数据"""
            # 设备开关
            if self.sku_instance == "powerSwitch":
                cn_name = "设备开关"
                onoff_value = (-1, 1, 0, 1, 2)
                for value_on in onoff_value:
                    api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value_on, cn_name)
            # 摇头
            elif self.sku_instance == "oscillationToggle":
                cn_name = "摇头"
                onoff_value = (-1, 1, 0, 1, 2)
                for value_on in onoff_value:
                    api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value_on, cn_name)
            # 夜灯开关
            elif self.sku_instance == "nightlightToggle":
                cn_name = "夜灯开关"
                onoff_value = (-1, 1, 0, 1, 2)
                for value_on in onoff_value:
                    api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value_on, cn_name)
            # 摆叶
            elif self.sku_instance == "airDeflectorToggle":
                cn_name = "摆叶"
                onoff_value = (-1, 1, 0, 1, 2)
                for value_on in onoff_value:
                    api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value_on, cn_name)
            # 目标温度
            elif self.sku_instance == "sliderTemperature":
                cn_name = "水壶目标温度"
                random_value_Celsius = random.randint(40, 100)
                random_value_Celsius1 = random.randint(40, 100)

                random_value_Fahrenheit = random.randint(104, 212)
                random_value_Fahrenheit1 = random.randint(104, 212)
                auto_value_list = [(random_value_Celsius, 'Celsius'),
                                   (random_value_Celsius1, 'Celsius'),
                                   (39, 'Celsius'),
                                   (101, 'Celsius'),
                                   (random_value_Fahrenheit, 'Fahrenheit'),
                                   (random_value_Fahrenheit1, 'Fahrenheit'),
                                   (103, 'Fahrenheit'),
                                   (213, 'Fahrenheit'),
                                   ]
                for value_auto in auto_value_list:
                    api.auto_mode_api(self.sku, self.device, self.sku_type, self.sku_instance,
                                      value_auto[0],
                                      value_auto[1], cn_name)
            elif self.sku_instance == "targetTemperature":
                cn_name = "目标温度"
                if "H713" in self.sku:
                    random_value_Celsius = random.randint(5, 30)
                    random_value_Celsius1 = random.randint(5, 30)
                    value_Celsius_err = random.randint(-10, 4)
                    value_Celsius_err1 = random.randint(31, 100)
                    random_value_Fahrenheit = random.randint(41, 86)
                    random_value_Fahrenheit1 = random.randint(41, 86)
                    value_Fahrenheit_err = random.randint(-10, 40)
                    value_Fahrenheit_err1 = random.randint(87, 100)
                    auto_value_list = [(random_value_Celsius1, 'Celsius', 0),
                                       (random_value_Celsius, 'Celsius', 1),
                                       (random_value_Celsius, 'Celsius', 0),
                                       (random_value_Celsius1, 'Celsius', 1),
                                       (value_Celsius_err, 'Celsius', 1),
                                       (value_Celsius_err1, 'Celsius', 1),
                                       (random_value_Fahrenheit1, 'Fahrenheit', 0),
                                       (random_value_Fahrenheit, 'Fahrenheit', 1),
                                       (random_value_Fahrenheit, 'Fahrenheit', 0),
                                       (random_value_Fahrenheit1, 'Fahrenheit', 1),
                                       (value_Fahrenheit_err, 'Fahrenheit', 1),
                                       (value_Fahrenheit_err1, 'Fahrenheit', 1)
                                       ]
                    for value_auto in auto_value_list:
                        api.auto_mode_api(self.sku, self.device, self.sku_type, self.sku_instance,
                                          value_auto[0],
                                          value_auto[1], cn_name, value_auto[2])
            # 夜灯场景
            elif self.sku_instance == "nightlightScene":
                cn_name = "夜灯场景"
                self.sku_value_enum = mode_type['parameters']['options']
                for i in self.sku_value_enum:
                    value = i['value']
                    api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value, cn_name)
            # 模式，档位
            elif self.sku_instance == "workMode":
                cn_name = "模式/档位"
                # api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, 0, "设备关机")  # 设备关机
                if "H713" in self.sku:
                    if self.sku == "H713A" or self.sku == "H7130":
                        mode_list = [0, 1, 2, 3, 4]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode)
                    else:
                        mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (9, 0), (3, 0)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                elif "H714" in self.sku:
                    mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
                                 (1, 10), (2, 0),
                                 (3, 0)]
                    for mode in mode_list:
                        self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                           mode[0],
                                           mode[1])
                elif "H716" in self.sku:
                    mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
                                 (1, 10), (2, 0), (3, 0)]
                    for mode in mode_list:
                        self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                           mode[0],
                                           mode[1])
                elif "H717" in self.sku:
                    if self.sku in ["H7170", "H7175"]:
                        mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0), (3, 0), (4, 0),
                                     (5, 0), (6, 0)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                    elif self.sku == "H7173":
                        mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0), (2, 1), (3, 0),
                                     (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 0), (4, 1), (4, 2), (4, 3),
                                     (4, 4), (4, 5)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                    elif self.sku == "H7171":
                        mode_list = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                    elif self.sku == "H7172":   # 制冰机
                        mode_list = [(1, 0), (2, 0), (3, 0), (4, 0)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                elif "H712" in self.sku:
                    if self.sku == "H7120":
                        mode_list = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (5, 0)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                    elif self.sku == "H7126":
                        mode_list = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (3, 0)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                    elif self.sku == "H7121":
                        mode_list = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (16, 0)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                    elif self.sku == "H7123":
                        mode_list = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (3, 0), (5, 0)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                    elif self.sku == "H7122":
                        mode_list = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2),
                                     (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11),
                                     (2, 12), (2, 13), (2, 14), (3, 0), (3, 1), (5, 0), (5, 1)]
                        for mode in mode_list:
                            self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                               mode[0],
                                               mode[1])
                elif "H715" in self.sku:
                    mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (3, 0), (8, 0), (1, 1)]
                    for mode in mode_list:
                        self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                           mode[0],
                                           mode[1])
                elif "H710" or "H711" in self.sku:
                    mode_list = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
                                 (2, 0), (3, 0),
                                 (5, 0), (6, 0), (7, 0)]
                    for mode in mode_list:
                        self.work_mode_api(self.sku, self.device, self.sku_type, self.sku_instance, cn_name,
                                           mode[0],
                                           mode[1])
            # 夜灯亮度
            elif self.sku_instance == "brightness":
                value_max = random.randint(1, 100)
                for value in [value_max, 1, 100, 0, 101]:
                    print("夜灯亮度:", value)
                    api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value)
            # 夜灯颜色
            elif self.sku_instance == "colorRgb":
                # result = (255 << 16) + (255 << 8) + 255  # 颜色算法
                value_max = random.randint(1, 16777215)
                for value in [16711680, 65280, 255, 1,value_max, 16777215, 16777216]:
                    print("夜灯颜色:", value)
                    api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value)
            # 加湿器 热雾
            elif self.sku_instance == "hotFogToggle":
                cn_name = "热雾"
                hotFogToggle = (1, 0)
                for value_on in hotFogToggle:
                    api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value_on, cn_name)
            # 目标湿度
            elif self.sku_instance == "humidity":
                cn_name = "目标湿度"
                random_value = random.randint(40, 70)
                auto_value_list = [random_value, -1, 0, 1, 100]
                for value in auto_value_list:
                    api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value, cn_name)
            elif self.sku_instance == "lightScene":
                if self.sku == 'H7161':
                    for value in [12549,12550, 12551, 12552, 12553,12554, 12555, 12556,12557,12558,12559,12560,12561,12562]:
                        print("夜灯颜色:", value)
                        api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value)
                elif self.sku == 'H7162':
                    for value in [12631, 12632, 12633, 12634, 12635, 12636, 12637, 12638, 12639, 12640,
                                  12641, 12642, 12643, 12644]:
                        print("夜灯颜色:", value)
                        api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, value)
            # 除湿机满水事件
            elif self.sku_instance == "waterFullEvent":
                cn_name = "除湿机满水事件"
                api.enum_api(self.sku, self.device, self.sku_type, self.sku_instance, 1, cn_name)
        print("\n")

    def enum_api(self, sku, device, sku_type, instance, value, cnname=None):

        """
        :param sku:   ALL
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

            print("send->:", power_json)
            if self.services =="qa":
                response = requests.post(url="https://openapi.api.govee.com/router/api/v1/device/control",
                                         headers=self.headers,
                                         json=power_json)
            else:
                response = requests.post(url="https://test-openapi.api.govee.com/router/api/v1/device/control",
                                     headers=self.headers,
                                     json=power_json)

            print("receive->", response.text)
            if "200" in str(response):
                if 'failure' in json.loads(response.text)['capability']['state']['status']:
                    print(str(cnname) + "：[" + str(value) + "]---->失败")
                    print('\n')
                else:
                    print(str(cnname) + "：[" + str(value) + "]---->成功")
                    print('\n')
            elif "429" in str(response):
                print("Status：429 Too Many Requests")

        except Exception as e:
            print(e)
            # pass
        time.sleep(5)

    def work_mode_api(self, sku, device, sku_type, instance, cnname, workModeValue, modeValue=None):

        """
        :param sku:  ALL
        :param device:
        :param sku_type:
        :param instance:
        :param value:
        :return: 模式、档位
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

            print("send->:", str(work_mode_json))
            if self.services == "qa":
                response = requests.post(url="https://openapi.api.govee.com/router/api/v1/device/control",
                                         headers=self.headers,
                                         json=work_mode_json)
            else:
                response = requests.post(url="https://test-openapi.api.govee.com/router/api/v1/device/control",
                                         headers=self.headers,
                                         json=work_mode_json)
            print("receive->", response.text)
            if "200" in str(response):
                if 'failure' in json.loads(response.text)['capability']['state']['status']:
                    print(str(cnname) + "[模式：" + str(workModeValue) + " 档位：" + str(modeValue) + "]---->失败")
                    print('\n')
                else:
                    print(str(cnname) + "[模式：" + str(workModeValue) + " 档位：" + str(modeValue) + "]---->成功")
                    print('\n')
            elif "429" in str(response):
                print("Status：429 Too Many Requests")

        except Exception as e:
            print(e)
            # pass
        time.sleep(5)

    def auto_mode_api(self, sku, device, sku_type, instance, temperature, unit, cnname, autoStop=None):

        """
        :param sku:  H713X  H714X H717X
        :param device:
        :param sku_type:
        :param instance:
        :param value:
        :return:  自动模式、目标温度值、自动停止开关
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
            print("send->:", mode_json)
            if self.services == "qa":
                response = requests.post(url="https://openapi.api.govee.com/router/api/v1/device/control",
                                         headers=self.headers,
                                         json=mode_json)
            else:
                response = requests.post(url="https://test-openapi.api.govee.com/router/api/v1/device/control",
                                         headers=self.headers,
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

            elif "429" in str(response):
                print("Status：429 Too Many Requests")
        except Exception as e:
            print(e)
            # pass
        time.sleep(5)

    # 状态查询
    def status_query(self,sku, device):
        """
        :param sku:
        :param device:
        :return:    查询状态
        """
        status_json = {
            "requestId": "1",
            "payload": {
                "sku": sku,
                "device": device,
            }
        }
        print("send->:", status_json)

        if self.services == "qa":
            response = requests.post(url="https://openapi.api.govee.com/router/api/v1/device/state",   # 正服
                                     headers=self.headers,
                                     json=status_json)
        else:
            response = requests.post(url="https://test-openapi.api.govee.com/router/api/v1/device/state",   # 测服
                                     headers=self.headers,
                                     json=status_json)
        print("receive->", response.text)
        # if "200" in str(response):
        #     print("receive->", json.loads(response.text)["capabilities"])


if __name__ == '__main__':
    # services = 'dev'
    sku = "H7131"
    services = 'qa'
    api = ApiTest(services,sku)   # 如果要测试账号下所有sku，就去掉传值sku
    # api = ApiTest(services)
    # while True:
    api.all_device()

