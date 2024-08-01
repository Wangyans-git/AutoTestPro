#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 提取iot关键字
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path

import openpyxl
import requests

import get_log


class ErpHandle:
    if not os.path.exists('./report/'):
        os.makedirs('./report/')

    def __init__(self):
        self.data = None
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
        path = str(Path(ROOT) / "lwt日志过滤/lwt过滤结果.log")
        self.get_log = get_log.GetLog(path)
        self.folder_path = os.path.dirname(os.path.abspath(__file__))
        self.filename = openpyxl.Workbook()
        self.result_file = r'{}\report\{}_{}.xlsx'.format(self.folder_path, "lwt过滤结果",
                                                          datetime.now().strftime('%Y-%m-%d_%H.%M.%S.%f'))
        self.sheet4 = self.filename.create_sheet(index=0, title="report")
        self.sheet = self.filename.create_sheet(index=1, title="掉线时间点")
        self.sheet2 = self.filename.create_sheet(index=2, title="回连时长")
        self.sheet3 = self.filename.create_sheet(index=3, title="stc")
        self.sheet5 = self.filename.create_sheet(index=4, title="stw")
        self.sheet6 = self.filename.create_sheet(index=5, title="oldA_stc_2")
        self.sheet7 = self.filename.create_sheet(index=6, title="ERR")

    def save_progress(self):
        self.filename.save(filename=self.result_file)
        print(f"Progress saved to {self.result_file}")

    def get_erp_data(self, devices_list):

        self.devices_count = 0

        for devices in range(0, len(devices_list)):
            stc_count = 0
            stw_count = 0
            self.oldA_rows = 0  # old行数
            self.oldA_2_count = 0  # stc中包含2的个数
            self.err_count = 0
            self.uqerr_count = 0
            self.umerr_count = 0
            self.uE0_count = 0
            self.rssi_avg = None
            self.devices_count += 1
            print("开始抓取{}".format(devices_list[devices]))
            print("共{}个，现在在第{}个".format(len(devices_list), self.devices_count))
            self.sheet.cell(1, 1).value = "aid"
            self.sheet.cell(2, 1).value = "sku"
            self.sheet.cell(3, 1).value = "uuid"
            self.sheet.cell(4, 1).value = "序号"
            self.sheet.cell(4, self.devices_count * 2).value = "掉线时间点"

            self.sheet2.cell(1, 1).value = "aid"
            self.sheet2.cell(2, 1).value = "sku"
            self.sheet2.cell(3, 1).value = "uuid"
            self.sheet2.cell(4, 1).value = "开始时间"
            self.sheet2.cell(5, 1).value = "结束时间"
            self.sheet2.cell(6, 1).value = "wifi_name"
            self.sheet2.cell(7, 1).value = "序号"
            self.sheet2.cell(7, self.devices_count * 3 - 1).value = "掉线时间点"
            self.sheet2.cell(7, self.devices_count * 3).value = "回连时长(单位:秒)"

            self.sheet3.cell(1, 1).value = "aid"
            self.sheet3.cell(2, 1).value = "sku"
            self.sheet3.cell(3, 1).value = "uuid"
            self.sheet3.cell(4, 1).value = "序号"
            self.sheet3.cell(4, self.devices_count * 2).value = "stc"

            self.sheet5.cell(1, 1).value = "aid"
            self.sheet5.cell(2, 1).value = "sku"
            self.sheet5.cell(3, 1).value = "uuid"
            self.sheet5.cell(4, 1).value = "序号"
            self.sheet5.cell(4, self.devices_count * 2).value = "stw"

            self.sheet4.cell(1, 1).value = "序号"
            self.sheet4.cell(1, 2).value = "aid"
            self.sheet4.cell(1, 3).value = "sku"
            self.sheet4.cell(1, 4).value = "uuid"
            self.sheet4.cell(1, 5).value = "开始时间"
            self.sheet4.cell(1, 6).value = "结束时间"
            self.sheet4.cell(1, 7).value = "wifi_name"
            self.sheet4.cell(1, 8).value = "掉线次数"
            self.sheet4.cell(1, 9).value = "平均信号强度"
            rssi_list = []

            self.num_all += 1
            # print("第{}个".format(self.num_all))
            self.device_name = devices_list[devices].replace(":", "")  # 格式化文件名
            erp_text_all = []
            self.time_list = []
            self.start_end_time = []
            self.device_wifiname = None

            for i in range(0, 2):
                json_erp = {
                    "device": devices_list[devices],
                    "searchType": 12,
                    "pageSize": 100,
                    "pageNum": i + 1,
                    # "endTime": 1705593600000,
                    # "startTime": 1709726400000
                }
                json_erp_device = {
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

                # 获取aid
                self.response_aid = requests.post(
                    # 正服
                    url='https://pro-appadmin-api.igovee.com/data-analysis/agg/search', headers=self.headers,
                    json=json_erp_device)
                # 测服
                # url='https://dev-appadmin-api.igovee.com/data-analysis/agg/search', headers=self.headers, json=json_erp)
                erp_text_aid = json.loads(self.response_aid.text)
                try:
                    self.device_uuid = devices_list[devices]
                    self.device_aid = erp_text_aid['data']['data']['list'][0]['data']['accountId']
                    self.device_sku = erp_text_aid['data']['data']['list'][0]['data']['sku']
                    self.device_wifiname = erp_text_aid['data']['data']['list'][0]['data']['settings']['wifiName']
                except Exception:
                    pass
                print(self.device_aid)
                # self.get_log.info("aid:{0}".format(self.device_aid))
                # self.get_log.info("sku:{0}".format(self.device_sku))
                # self.get_log.info("uuid:{}".format(self.device_uuid))

                for self.data in erp_text['data']['data']['list']:
                    # print("data:{}".format(data))
                    # self.get_log.info("data:{}".format(data))
                    time_erp = self.data['timestamps']
                    self.start_end_time.append(time_erp)

                    try:
                        stw = self.data['data']['message']['state']['sta']['stw']
                        stw_count += 1
                        self.sheet5.cell(stc_count + 4, 1).value = stw_count
                        self.sheet5.cell(1, self.devices_count * 2).value = self.device_aid
                        self.sheet5.cell(2, self.devices_count * 2).value = self.device_sku
                        self.sheet5.cell(3, self.devices_count * 2).value = self.device_uuid
                        self.sheet5.cell(stc_count + 4, self.devices_count * 2).value = stw
                    except Exception:
                        pass

                    try:
                        stc = self.data['data']['message']['state']['sta']['stc']
                        #
                        # print('stc:{}'.format(stc))
                        rssi = re.split('_', stc)[2]  # 信号值

                        rssi_list.append(int(rssi))
                        # print("rssi_list:{}".format(rssi_list))

                        # self.stc = data['message']['state']['sta']['stc']   # 提取stc

                        stc_count += 1
                        # self.start_end_time.append(stc)
                        #     self.get_log.info("stc:{0}".format(stc))

                        self.sheet3.cell(stc_count + 4, 1).value = stc_count
                        self.sheet3.cell(1, self.devices_count * 2).value = self.device_aid
                        self.sheet3.cell(2, self.devices_count * 2).value = self.device_sku
                        self.sheet3.cell(3, self.devices_count * 2).value = self.device_uuid
                        self.sheet3.cell(stc_count + 4, self.devices_count * 2).value = stc
                    except Exception:
                        pass

                    self.err()
                    self.filename.save(self.result_file)
                    # data_erp = data['data']
                    # self.data_erp_sku = data['data']['sku']
                    # print(time_erp)
                    # if "LWT" in str(data):  # 过滤掉LWT日志
                    #     erp_text_all.append(data)
                    # else:
                    #     pass
                # try:
                #     self.rssi_avg = sum(rssi_list) / len(rssi_list)
                #     print('rssi_平均值:{:.2f}'.format(self.rssi_avg))
                # except Exception:
                #     pass
                if "True" in str(erp_text['data']['data']['hasNext']):
                    print("第{}页".format(i + 1))
                else:
                    print("第{}页,最后一页".format(i + 1))
                    break
            # print(erp_text_all)
            erp_text_all.reverse()  # 翻转时间
            count_fail = 0
            # for connected in erp_text_all:
            #
            #     # print(connected)
            #     if "'connected': 0" in str(connected):
            #         count_fail += 1
            #         # print(str(connected))
            #         # self.get_log.info("'connected': 0:{}".format(str(connected)))
            #         # print(connected['timestamps'])
            #         # self.get_log.info("'connected': 0:{0}".format(connected))
            #         # print("connected:", connected['data']['connected'])
            #         down_time = connected['timestamps']
            #         # 将字符串转换为datetime对象
            #         time_obj = datetime.strptime(down_time, "%Y-%m-%d %H:%M:%S")
            #         # 提取年、月、日、时、分、秒的值
            #         year = time_obj.year
            #         month = time_obj.month
            #         day = time_obj.day
            #         hour = time_obj.hour
            #         minute = time_obj.minute
            #         second = time_obj.second
            #         # 输出结果
            #         self.down_time_str = datetime(year, month, day, hour, minute, second)
            #         # print("下线时间------：", self.down_time_str)
            #         # self.get_log.info("第{}次下线时间点-：{}".format(count_fail, self.down_time_str))
            #         self.time_list.append(connected['data']['connected'])
            #         self.time_list.append(self.down_time_str)
            #
            #         self.sheet.cell(count_fail + 4, 1).value = count_fail
            #         self.sheet.cell(1, self.devices_count * 2).value = self.device_aid
            #         self.sheet.cell(2, self.devices_count * 2).value = self.device_sku
            #         self.sheet.cell(3, self.devices_count * 2).value = self.device_uuid
            #         self.sheet.cell(count_fail + 4, self.devices_count * 2).value = self.down_time_str
            #         self.filename.save(self.result_file)
            #     elif "'connected': 1" or "'connected': 2" == str(connected):
            #         # print(connected['timestamps'])
            #         # print("connected:", connected['data']['connected'])
            #         up_time = connected['timestamps']
            #         # 将字符串转换为datetime对象
            #         time_obj = datetime.strptime(up_time, "%Y-%m-%d %H:%M:%S")
            #         # 提取年、月、日、时、分、秒的值
            #         year = time_obj.year
            #         month = time_obj.month
            #         day = time_obj.day
            #         hour = time_obj.hour
            #         minute = time_obj.minute
            #         second = time_obj.second
            #         # 输出结果
            #         self.up_time_str = datetime(year, month, day, hour, minute, second)
            #         # print("上线时间：", self.up_time_str)
            #         self.time_list.append(connected['data']['connected'])
            #         self.time_list.append(self.up_time_str)
            # # print(self.time_list)
            # self.result = {}
            # for i in range(0, len(self.time_list), 2):
            #     value = self.time_list[i]
            #     key = self.time_list[i + 1]
            #     self.result[key] = value

            # self.handle_lwt(self.result)    # 过滤lwt数据操作
            self.filename.save(self.result_file)
            print("保存完成")
            time.sleep(6)
        return self.device_sku, self.device_aid, self.rssi_avg, self.data

    def oldA(self):
        # oldA+stc2
        self.sheet6.cell(1, 1).value = "aid"
        self.sheet6.cell(2, 1).value = "sku"
        self.sheet6.cell(3, 1).value = "uuid"
        self.sheet6.cell(4, 1).value = "oldA和2同时出现次数"
        # self.sheet6.cell(5, 1).value = "序号"
        # self.sheet6.cell(5, self.devices_count * 2).value = "stc"
        # sheet = '{}_{}'.format(sheet, j)
        try:
            oldA = self.data['data']['from']
            stc = self.data['data']['message']['state']['sta']['stc']
            stc_2 = re.split('_', stc)[1]  # 重启类型值
            self.oldA_rows += 1
            if oldA == "oldA":
                if stc_2 == "2":
                    self.oldA_2_count += 1
            # self.sheet6.cell(oldA_rows + 5, 1).value = oldA_rows
            self.sheet6.cell(1, self.devices_count + 1).value = self.device_aid
            self.sheet6.cell(2, self.devices_count + 1).value = self.device_sku
            self.sheet6.cell(3, self.devices_count + 1).value = self.device_uuid
            self.sheet6.cell(4, self.devices_count + 1).value = self.oldA_2_count
            # self.sheet6.cell(oldA_rows + 5, self.devices_count * 2).value = oldA
        except Exception:
            pass

    def err(self):
        # err
        self.sheet7.cell(1, 1).value = "aid"
        self.sheet7.cell(2, 1).value = "sku"
        self.sheet7.cell(3, 1).value = "uuid"
        self.sheet7.cell(4, 1).value = "err_all"
        self.sheet7.cell(5, 1).value = "uE0"
        self.sheet7.cell(6, 1).value = "uqerr"
        self.sheet7.cell(7, 1).value = "umerr"

        # self.sheet6.cell(5, 1).value = "序号"
        # self.sheet6.cell(5, self.devices_count * 2).value = "stc"

        try:
            uqerr = self.data['data']['message']['uqerr']
            umerr = self.data['data']['message']['umerr']
            uE0 = self.data['data']['message']['uE0']
            if umerr == 1:
                self.umerr_count += 1
                self.err_count += 1
            if uE0 == 1:
                self.uE0_count += 1
                self.err_count += 1
            if uqerr == 1:
                self.uqerr_count += 1
                self.err_count += 1

            # self.sheet6.cell(oldA_rows + 5, 1).value = oldA_rows
            self.sheet7.cell(1, self.devices_count + 1).value = self.device_aid
            self.sheet7.cell(2, self.devices_count + 1).value = self.device_sku
            self.sheet7.cell(3, self.devices_count + 1).value = self.device_uuid
            self.sheet7.cell(4, self.devices_count + 1).value = self.err_count
            self.sheet7.cell(5, self.devices_count + 1).value = self.uE0_count
            self.sheet7.cell(6, self.devices_count + 1).value = self.uqerr_count
            self.sheet7.cell(7, self.devices_count + 1).value = self.umerr_count

            # self.sheet6.cell(oldA_rows + 5, self.devices_count * 2).value = oldA
        except Exception:
            pass

    # 过滤lwt数据
    def handle_lwt(self, erp_data):
        # 上线时长

        try:
            self.log_start_time = self.start_end_time[-1]
            self.log_end_time = self.start_end_time[0]

            print("开始时间：{0}".format(self.log_start_time))
            print("结束时间：{0}".format(self.log_end_time))
            # self.get_log.info("开始时间：{0}".format(self.log_start_time))
            # self.get_log.info("结束时间：{0}".format(self.log_end_time))
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
        self.online_num = 0
        # print("result_online",result_online)
        for i in result_online:
            # print(i)
            if len(i) >= 2:
                online_time = i[0]  # 掉线时间
                offline_time = i[1]  # 在线时间
                self.online_duration = offline_time - online_time
                time_str = self.online_duration.total_seconds()
                # print(online_time)
                # off_to_online.append(self.online_duration)  # 掉线最后结果汇总
                # print("第{0}次掉线后上线回连时长：{1}".format(self.online_num, self.online_duration))
                # self.get_log.info("aid:{},sku:{}，第{}次回连耗时：{}".format(self.device_aid, self.device_sku, self.online_num, self.online_duration))
                print("aid:{},sku:{}，{},第{}次回连耗时：{}".format(self.device_aid, self.device_sku, online_time,
                                                                  self.online_num,
                                                                  self.online_duration))

                try:
                    self.sheet2.cell(4, self.devices_count * 3 - 1).value = self.log_start_time
                    self.sheet2.cell(5, self.devices_count * 3 - 1).value = self.log_end_time
                    self.sheet2.cell(6, self.devices_count * 3 - 1).value = self.device_wifiname
                except Exception:
                    pass
                self.sheet2.cell(self.online_num + 7, 1).value = self.online_num
                self.sheet2.cell(1, self.devices_count * 3 - 1).value = self.device_aid
                self.sheet2.cell(2, self.devices_count * 3 - 1).value = self.device_sku
                self.sheet2.cell(3, self.devices_count * 3 - 1).value = self.device_uuid
                self.sheet2.cell(self.online_num + 7, self.devices_count * 3 - 1).value = online_time
                self.sheet2.cell(self.online_num + 7, self.devices_count * 3).value = time_str
                self.online_num += 1

            else:
                pass
            self.filename.save(self.result_file)
        try:
            self.sheet4.cell(self.devices_count + 1, 1).value = self.devices_count
            self.sheet4.cell(self.devices_count + 1, 2).value = self.device_aid
            self.sheet4.cell(self.devices_count + 1, 3).value = self.device_sku
            self.sheet4.cell(self.devices_count + 1, 4).value = self.device_uuid
            self.sheet4.cell(self.devices_count + 1, 5).value = self.log_start_time
            self.sheet4.cell(self.devices_count + 1, 6).value = self.log_end_time
            self.sheet4.cell(self.devices_count + 1, 7).value = self.device_wifiname
            self.sheet4.cell(self.devices_count + 1, 8).value = self.online_num
            self.sheet4.cell(self.devices_count + 1, 9).value = '{:.2f}'.format(self.rssi_avg)
        except Exception:
            pass
        self.filename.save(self.result_file)
        print("=======================================================")


# 关闭文件
# wb.close()

if __name__ == '__main__':
    erp = ErpHandle()

    # devices_list = ["3A:B0:D4:AD:FC:C7:ED:3C"]
    devices_list = ["23:B3:60:74:F4:FC:3E:EC", "2E:C7:60:74:F4:FC:79:4A"]

    # ['0A:7B:54:32:04:41:B8:FC','21:76:54:32:04:43:32:68','37:31:54:32:04:44:74:E4']

    # ['5B:98:54:32:04:D2:8C:3C', '11:0B:60:74:F4:73:30:88']
    # ["0F:C4:54:32:04:D0:27:D4", "5B:98:54:32:04:D2:8C:3C","11:C8:54:32:04:D2:5E:08"] # , "0F:C4:54:32:04:D0:27:D4", "5B:98:54:32:04:D2:8C:3C","11:C8:54:32:04:D2:5E:08"
    erp.get_erp_data(devices_list)
