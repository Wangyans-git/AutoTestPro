#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @Description : 取暖器接口抓取日志。过滤LWT日志
import time
from pathlib import Path

import requests
import json
# from Handle_erp.tool.mqtt_split_tool_H7132 import Log_Prase_Handle
# from Handle_erp.tool import mqtt_split_tool_H7132

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
log_file = str(Path(ROOT) / "")


# print(log_file)


class ErpHandle:
    def __init__(self, formal_test_flag):
        self.formal_test_flag = formal_test_flag
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            # 正服
            "Authorization": "",
            # 测服
            # "Authorization": "",
            "originFrom": "decode_erp",
            "Content-Length": "80",
            "Origin": "https://erp.lanjingerp.com",
            "Connection": "keep-alive",
            "Referer": "https://erp.lanjingerp.com/",
        }
        if self.formal_test_flag:
            self.headers[
                "Authorization"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblRpbWUiOjE2OTg5MjU2MjMsImlzcyI6Imlob21lbnQiLCJ1c2VySWQiOjE2NzYsInVzZXJuYW1lIjoieXVfY2FvIn0.X73nr-2sJqcv-aftkXbPpQMLET05-y0QtTWKNjsMW7Q"
        else:
            self.headers[
                "Authorization"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblRpbWUiOjE2OTg5ODIzMTUsImlzcyI6Imlob21lbnQiLCJ1c2VySWQiOjQwODgsInVzZXJuYW1lIjoid2FuZ195YW5zaGVuZyJ9.ert-kBgLVp3J9BEysTg2G_xekey8i9VtSuJUxJ47s2Q"
        self.device_name = ""
        self.page_num = 0
        self.num = 0
        self.num_all = 0
        self.devices_list = []
        self.erp_text_all = ''
        self.test = ''

    def get_device(self, get_aid=None, get_sku=None):

        json_device = {
            "accountId": get_aid,
            "searchType": "2",
            "pageSize": 100,
            "pageNum": 1
        }
        json_phone_list = {
            "accountId": get_aid,
            "searchType": "4",
            "pageSize": 100,
            "pageNum": 1
        }

        if self.formal_test_flag:
            self.response = requests.post(
                # 正服
                url='https://pro-appadmin-api.igovee.com/data-analysis/agg/search', headers=self.headers,
                json=json_device)
            time.sleep(1)
            self.response_phone_list = requests.post(
                # 正服
                url='https://pro-appadmin-api.igovee.com/data-analysis/agg/search', headers=self.headers,
                json=json_phone_list)
            time.sleep(1)
        else:
            # 测服
            self.response = requests.post(url='https://dev-appadmin-api.igovee.com/data-analysis/agg/search',
                                          headers=self.headers,
                                          json=json_device)
            self.response_phone_list = requests.post(url='https://dev-appadmin-api.igovee.com/data-analysis/agg/search',
                                                     headers=self.headers,
                                                     json=json_phone_list)
        erp_device_text = json.loads(self.response.text)
        erp_phone_list = json.loads(self.response_phone_list.text)
        # print(erp_device_text)
        for device_all in erp_device_text['data']['data']['list']:
            # print(device_all)
            device = device_all['data']['device']
            sku = device_all['data']['sku']
            if sku == get_sku:
                self.devices_list.append(device)



    def get_erp(self, aid=None, sku=None):

        self.get_device(aid, sku)
        if not self.devices_list:
            print(f"没有{sku}")
        for devices in range(0, len(self.devices_list)):
            self.num_all += 1
            # print("第{}个".format(self.num_all))
            self.device_name = self.devices_list[devices].replace(":", "")  # 格式化文件名
            print("开始抓取{0}".format(self.devices_list[devices]))
            for i in range(0, 1000):
                json_erp = {
                    "device": self.devices_list[devices],
                    "searchType": 12,
                    "pageSize": 1000,
                    "pageNum": i + 1
                }

                if self.formal_test_flag:
                    self.response = requests.post(
                        # 正服
                        url='https://pro-appadmin-api.igovee.com/data-analysis/agg/search', headers=self.headers,
                        json=json_erp)

                else:
                    # 测服
                    self.response = requests.post(url='https://dev-appadmin-api.igovee.com/data-analysis/agg/search',
                                                  headers=self.headers,
                                                  json=json_erp)
                erp_text = json.loads(self.response.text)
                # print(erp_text)
                for data in erp_text['data']['data']['list']:
                    time_erp = data['timestamps']
                    data_erp = data['data']
                    self.data_erp_sku = data['data']['sku']
                    # if data_erp['bizType'] == "LWT":  # 过滤掉LWT日志
                    #     pass
                    # else:
                    self.erp_text_all += (str(time_erp) + "\n").replace("'", '"')
                    self.erp_text_all += '\n'
                    self.erp_text_all += (str(data_erp) + "\n").replace("'", '"').replace(" ", "") \
                        .replace("True", "true").replace('"message":{', '"message":"{') \
                        .replace('},"@timestamp"', '}","@timestamp"')
                if "True" in str(erp_text['data']['data']['hasNext']):
                    print("第{}页".format(i + 1))
                else:
                    print("第{}页,最后一页".format(i + 1))
                    break
            if self.erp_text_all != "":
                try:
                    # with open("tool/in_log.txt", "w") as file:
                    #     file.write(self.erp_text_all)
                    with open(f"原始数据\\{self.data_erp_sku}_{aid}_{self.device_name}.txt", "w") as file:
                        # with open(f"原始数据\\{self.data_erp_sku}_{self.device_name}.txt", "w") as file:
                        file.write(self.erp_text_all)
                    # self.num += 1
                    # print(f"已爬{0}".format(self.num))
                except Exception as e:
                    pass

                    # print(e)
                    # print("没日志")
                time.sleep(1)

            else:
                print("没日志")
            time.sleep(5)
        # mqtt_split_tool_H7132.Log_Prase_Handle()  # 解析日志

        # self.dingdingrobot()

    def dingdingrobot(self):
        robot_text = {
            "msgtype": "text",
            "text": {
                # "content": self.test
                "content": "测试"
            }
        }
        requests.post(
            url='https://oapi.dingtalk.com/robot/send?access_token=6d1b244b17a8360d971c7ba5b043ade76badf951b2f973729e'
                '8dab31f624db81',
            headers=self.headers,
            json=robot_text)
        time.sleep(1)


if __name__ == '__main__':
    sku = 'H7135'
    aid = "3873253"
    formal_test = 1  # 1正服  0测服
    erp = ErpHandle(formal_test)
    erp.get_erp(aid, sku)

