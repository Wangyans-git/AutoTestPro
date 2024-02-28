#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : Base64日志分析工具
import base64
import binascii
import os
import re
import time
from Iot数据整理.get_log import GetLog

class Iot:
    def __init__(self):
        self.get_log = GetLog("IOT日志分析H7135_log.log")

    def traverse_files(self,directory):
        file_list = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path)

        return file_list

    # 抓取关键字日志
    def extract_data_around_keyword(self,file_path, keyword_list, window_size):
        with open(file_path, 'r') as file:
            content = file.read()

        extracted_data = []

        for keyword in keyword_list:
            index = 0

            while index < len(content):
                start_index = content.find(keyword, index)

                if start_index == -1:
                    break

                end_index = start_index + len(keyword)
                # left_boundary = max(0, start_index - window_size)
                left_boundary = max(0, start_index - 35)   # 关键字左边文字数量，数值越大数量越多
                right_boundary = min(len(content), end_index + window_size)
                extracted_data.append(content[left_boundary:right_boundary])

                index = end_index
        return extracted_data

    def read_iot_text(self,file):
        # 打开文件
        with open(file, 'r') as file:
            # 读取文件内容
            content = file.read()
        # 输出文件内容
        return content


if __name__ == '__main__':
    iot = Iot()
    time_directory = r'C:\Users\王衍升\Desktop\IOT日志分析\H7143_6564492_29026074F43AB6EA.txt'  # 替换为实际的目录路径
    file_all= iot.read_iot_text(time_directory)
    # print(file_all)
    iot_pattern = r'"([^"]+=)"'
    time_pattern = r"\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b"
    time_matches = re.findall(time_pattern, file_all)
    # print(time_matches)
    iot_matches = re.findall(iot_pattern, file_all)
    # print(iot_matches)
    data_list = []
    iot_num = len(time_matches)
    print("时间个数：", iot_num)
    for i in range(iot_num):
        print(time_matches[i])
        for j in iot_matches:
            print(j)
    # for file_path in file_list:
    #     for iot_time in time_matches:  # 遍历每一组数据的时间
        #     print(iot_time)
        #     iot.get_log.info(iot_time)
        # for item in data:
            # print(item)

            # matches = re.findall(pattern, item)
            #
            # for i in matches:
            #     # print(i)
            #     if "=" in i:
            #         decoded_data = base64.b64decode(i)
            #         hex_data = binascii.hexlify(decoded_data)
            #         # print(hex_data)
            #         iot.get_log.info(hex_data)
            # print("============================================")
            # if "timestamp" in item:
            #     break
