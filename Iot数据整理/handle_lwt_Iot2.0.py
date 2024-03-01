#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 提取iot关键字
import re
import time
# import openpyxl
import requests
import json

from datetime import datetime
# from openpyxl import Workbook, load_workbook
# from openpyxl import Workbook
import get_log
# from Handle_erp.tool.mqtt_split_tool import Log_Prase_Handle
from pathlib import Path


# 创建一个新的 Excel 工作簿
# workbook = Workbook()

# 选择第一个工作表
# sheet = workbook.active

# 在第一行插入表头
# sheet.append(["掉线时间", "上线时间", "重连时长"])


class ErpHandle:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            # 正服
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblRpbWUiOjE2OTg5MjU2MjMsImlzcyI6Imlob21lbnQiLCJ1c2VySWQiOjE2NzYsInVzZXJuYW1lIjoieXVfY2FvIn0.X73nr-2sJqcv-aftkXbPpQMLET05-y0QtTWKNjsMW7Q",
            # 测服
            # "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblRpbWUiOjE2OTg5ODIzMTUsImlzcyI6Imlob21lbnQiLCJ1c2VySWQiOjQwODgsInVzZXJuYW1lIjoid2FuZ195YW5zaGVuZyJ9.ert-kBgLVp3J9BEysTg2G_xekey8i9VtSuJUxJ47s2Q",
            "originFrom": "decode_erp",
            "Content-Length": "80",
            "Origin": "https://erp.lanjingerp.com",
            "Connection": "keep-alive",
            "Referer": "https://erp.lanjingerp.com/",
        }
        self.device_name = ""
        self.page_num = 0
        self.num = 0
        self.num_all = 0
        self.up_time_str = ''
        self.down_time_str = ''
        FILE = Path(__file__).resolve()
        ROOT = FILE.parents[1]  # YOLOv5 root directory
        path = str(Path(ROOT) / "Iot数据整理/lwt过滤结果.log")
        self.get_log = get_log.GetLog(path)
        self.erp_text_all = []
        self.time_list = []  # 时间列表
        self.start_end_time = []

    def get_erp_data(self, devices_list):

        for devices in range(0, len(devices_list)):
            soft_reboot_num = 0  # 软件重启次数
            olda_num = 0
            print("开始抓取{}".format(devices_list[devices]))

            self.num_all += 1
            # print("第{}个".format(self.num_all))
            self.device_name = devices_list[devices].replace(":", "")  # 格式化文件名

            for i in range(0, 99):
                json_erp = {
                    "device": devices_list[devices],
                    "searchType": 12,
                    "pageSize": 1000,
                    "pageNum": i + 1
                }
                json_erp_aid = {
                    "device": devices_list[devices],
                    "searchType": 11,
                }
                self.response = requests.post(
                    # 正服
                    url='https://pro-appadmin-api.igovee.com/data-analysis/agg/search', headers=self.headers,
                    json=json_erp)
                # 测服
                # url='https://dev-appadmin-api.igovee.com/data-analysis/agg/search', headers=self.headers, json=json_erp)
                erp_text = json.loads(self.response.text)
                # print(erp_text)
                # if "oldA" in str(erp_text):   # 过滤不包含oldA的数据
                # 获取aid
                self.response_aid = requests.post(
                    # 正服
                    url='https://pro-appadmin-api.igovee.com/data-analysis/agg/search', headers=self.headers,
                    json=json_erp_aid)
                # 测服
                # url='https://dev-appadmin-api.igovee.com/data-analysis/agg/search', headers=self.headers, json=json_erp)
                erp_text_aid = json.loads(self.response_aid.text)
                self.get_log.info(devices_list[devices])
                self.get_log.info("sku:{0}".format(erp_text_aid['data']['data']['list'][0]['data']['sku']))
                self.get_log.info("aid:{0}".format(erp_text_aid['data']['data']['list'][0]['data']['accountId']))
                for data in erp_text['data']['data']['list']:
                    try:
                        if str(data['data']['from']) == "oldA":
                            olda_num += 1
                            self.get_log.info("old A---:{}".format(data['timestamps']))
                    except Exception:
                        pass
                    try:
                        stc = data['data']['message']['state']['sta']['stc']
                        string = stc
                        pattern = r"\d+_(\d+)_\d+_\d+"
                        match = re.search(pattern, string)
                        if match:
                            result = match.group(1)
                            # print(type(result))
                            if int(result) >= 3:
                                soft_reboot_num += 1
                                self.get_log.info("stc:{}".format(stc))
                                self.get_log.info("stc:{0}---软件重启时间:{1}".format(result, data['timestamps']))
                    except Exception:
                        pass
                    time_erp = data['timestamps']
                    self.start_end_time.append(time_erp)  # 汇总开始和结束时间
                    # data_erp = data['data']
                    # self.data_erp_sku = data['data']['sku']
                    # print(time_erp)
                    if "LWT" in str(data):  # 过滤掉LWT日志
                        self.erp_text_all.append(data)
                    else:
                        pass
                # else:
                #     pass
                if "True" in str(erp_text['data']['data']['hasNext']):
                    print("第{}页".format(i + 1))
                else:
                    print("第{}页,最后一页".format(i + 1))
                    break
            # print(self.erp_text_all)
            if "oldA" in str(erp_text):
                self.get_log.info("软重启次数:{}".format(soft_reboot_num))
                self.get_log.info("old次数:{}".format(olda_num))
            self.erp_text_all.reverse()  # 翻转时间
            for connected in self.erp_text_all:
                # print(connected)
                if "'connected': 0" in str(connected):
                    # print(connected)
                    # print(connected['timestamps'])
                    print("connected:", connected['data']['connected'])
                    down_time = connected['timestamps']
                    # 将字符串转换为datetime对象
                    time_obj = datetime.strptime(down_time, "%Y-%m-%d %H:%M:%S")
                    # 提取年、月、日、时、分、秒的值
                    year = time_obj.year
                    month = time_obj.month
                    day = time_obj.day
                    hour = time_obj.hour
                    minute = time_obj.minute
                    second = time_obj.second
                    # 输出结果
                    self.down_time_str = datetime(year, month, day, hour, minute, second)
                    print("下线时间：", self.down_time_str)
                    # self.get_log.info("下线时间：{0}".format(self.down_time_str))
                    self.time_list.append(connected['data']['connected'])
                    self.time_list.append(self.down_time_str)
                elif "'connected': 1" or "'connected': 2" in str(connected):
                    # print(connected['timestamps'])
                    print("connected:", connected['data']['connected'])
                    up_time = connected['timestamps']
                    # 将字符串转换为datetime对象
                    time_obj = datetime.strptime(up_time, "%Y-%m-%d %H:%M:%S")
                    # 提取年、月、日、时、分、秒的值
                    year = time_obj.year
                    month = time_obj.month
                    day = time_obj.day
                    hour = time_obj.hour
                    minute = time_obj.minute
                    second = time_obj.second
                    # 输出结果
                    self.up_time_str = datetime(year, month, day, hour, minute, second)
                    print("上线时间：", self.up_time_str)
                    # self.get_log.info("上线时间：{0}".format(self.up_time_str))
                    self.time_list.append(connected['data']['connected'])
                    self.time_list.append(self.up_time_str)
            # print(self.time_list)
            self.result = {}
            for i in range(0, len(self.time_list), 2):
                value = self.time_list[i]
                key = self.time_list[i + 1]
                self.result[key] = value

            self.handle_lwt(self.result)

            time.sleep(3)

    # 过滤lwt数据
    def handle_lwt(self, erp_data):
        # 上线时长
        try:
            self.get_log.info("开始时间：{0}".format(self.start_end_time[-1]))
            self.get_log.info("结束时间：{0}".format(self.start_end_time[0]))
        except Exception:
            pass
        # off_to_online = []
        self.off_online_result_all = ""
        # 找到第一个值为0的键
        key_to_delete = None
        for key, value in erp_data.items():
            if value == 0:
                key_to_delete = key
                break

        # 删除键及其之前的所有键值对
        if key_to_delete is not None:
            keys_to_delete = list(erp_data.keys())[:list(erp_data.keys()).index(key_to_delete)]
            for key in keys_to_delete:
                del erp_data[key]

        # print("erp:",erp_data)
        erp_data.update({datetime(1111, 11, 11, 11, 11): 0})
        result_online = []
        group_online = []
        # 遍历列表
        for key, value in erp_data.items():
            if value == 0 and group_online:  # 如果下一位的key等于0或者不为空，就将前一组数据添加到总结果列表
                # print("group_online:", group_online)
                # if "0" not in str(erp_data[key]) :
                result_online.append(group_online)  # 将一组数据存入总结果列表
                group_online = []  # 并且清空小分组列表
            group_online.append(key)  # 每遍历一次列表添加一个数据，直到value=0

        # 打印结果
        online_num = 1
        # print("result_online",result_online)
        for i in result_online:
            # print(i)
            if len(i) >= 2:
                online_time = i[0]  # 掉线时间
                offline_time = i[1]  # 在线时间
                self.online_duration = offline_time - online_time
                # off_to_online.append(self.online_duration)  # 掉线最后结果汇总
                print("第{0}次掉线后上线回连时长：{1}".format(online_num, self.online_duration))
                # self.get_log.info("第{0}次掉线后上线回连时长：{1}".format(online_num, self.online_duration))
                online_num += 1
            else:
                pass

        # # print(result_online)

        # # 遍历数据列表，逐行插入数据
        # for row in off_to_online:
        #     sheet.append(row)
        #
        # # 保存 Excel 文件
        # workbook.save("data.xlsx")

        # # 掉线时长
        # result_offline = []
        # group_offline = []
        # # on_to_offline = []
        # # # 遍历列表
        # for key, value in self.result.items():
        #     # if group_offline:
        #     if value == 1 or value == 2:  # 如果下一位的key等于1 or 2 都添加到小分组数据
        #         group_offline.append(key)
        #     if value == 0:  # 如果下一位为0，就将该小分组加入总结果列表
        #         group_offline.append(key)
        #         if len(group_offline) >= 2:
        #             result_offline.append(group_offline)  # 将一组数据存入总结果列表
        #             print("group_offline:", group_offline)
        #         group_offline = []  # 并且清空小分组列表
        #
        # offline_num = 1
        # for i in result_offline:
        #     if len(i) >= 2:
        #         online_time = i[0]  # 最后在线时间
        #         offline_time = i[-1]  # 掉线时间
        #         self.offline_duration = offline_time - online_time
        #         # on_to_offline.append(self.offline_duration)
        #         # self.off_online_result_all += str(self.offline_duration) + "\n"
        #         # print("第{0}次掉线时长{1}".format(offline_num, self.offline_duration))
        #         # self.get_log.info("第{0}次掉线时长{1}".format(offline_num,self.offline_duration) )
        #         offline_num += 1+
        #     else:
        #         pass
        # print(result_offline)

        self.get_log.info("=======================================================")


# 关闭文件
# wb.close()

if __name__ == '__main__':
    erp = ErpHandle()
    devices_list = ["E5:B7:D8:32:37:36:51:23"]
    erp.get_erp_data(devices_list)
