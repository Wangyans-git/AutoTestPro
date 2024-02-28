#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 小家电API
import json
import time

import requests
import secrets


class ApiTest(object):
    def __init__(self):
        self.headers = {"Govee-API-Key": "e3d85d3d-eaa8-4070-b7e3-8ac64b33f9c1", "Content-Type": "application/json"}
        self.response = requests.get(
            url='https://dev-developer-api.govee.com/v1/appliance/devices', headers=self.headers)
        self.v = 0

    # 查询设备
    def all_device(self):
        date = json.loads(self.response.text)
        # print(date)
        str_data = json.dumps(date)
        print(str_data)
        sku_count = str_data.count('model')
        for i in range(sku_count):
            self.device = date['data']['devices'][i]['device']  # 设备id
            print("Device:", self.device)
            self.model = date['data']['devices'][i]['model']  # sku
            print("model:", self.model)
            self.mode_all = date['data']['devices'][i]['properties']['mode']['options']  # 模式
            print("mode_all:", self.mode_all)
            try:
                self.gear_all = date['data']['devices'][i]['properties']['gear']['options']  # 档位
                print("gear_all:", self.gear_all)
            except Exception:
                pass
            print("扫描到sku：", self.model)
            api.all_api()

    def all_api(self):
        # mode
        print("开始测试{}".format(self.model))
        # time.sleep(10)
        for i in self.mode_all:
            json = {
                "device": self.device,
                "model": self.model,
                "cmd": {
                    "name": "mode",
                    "value": i["value"]
                }
            }
            print("json:", json)
            response = requests.put(url="https://developer-api.govee.com/v1/appliance/devices/control",
                                    headers=self.headers,
                                    json=json)
            print(response)
            if 'Success' in response.text:
                print(str(i['name']) + "---->成功")
            else:
                print(str(i['name']) + "---->失败")
            time.sleep(5)

        # gear
        try:
            for i in self.gear_all:
                for self.v in range(len(i['value'])):
                    self.v += 1  # value值
                    json = {
                        "device": self.device,
                        "model": self.model,
                        "cmd": {
                            "name": "gear",
                            "value": self.v
                        }
                    }
                    response = requests.put(url='https://developer-api.govee.com/v1/appliance/devices/control',
                                            headers=self.headers,
                                            json=json)
                    print(response)
                    if 'Success' in response.text:
                        print(str(i['name'] + str(self.v)) + "---->成功")
                    else:
                        print(str(i['name'] + str(self.v)) + "---->失败")
                    time.sleep(5)
        except Exception:
            pass


if __name__ == '__main__':
    api = ApiTest()
    api.all_device()
