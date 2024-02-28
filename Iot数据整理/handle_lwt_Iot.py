#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 提取iot关键字

import os
import time


def traverse_files(directory):
    file_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    return file_list


# 抓取关键字日志
def extract_data_around_keyword(file_path, keyword_list, window_size):
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
            left_boundary = max(0, start_index - 32)   # 关键字左边文字数量，数值越大数量越多
            right_boundary = min(len(content), end_index + window_size)
            extracted_data.append(content[left_boundary:right_boundary])

            index = end_index
    return extracted_data


if __name__ == '__main__':
    directory = r'C:\Users\王衍升\Desktop\IOT日志分析'  # 替换为实际的目录路径
    file_list = traverse_files(directory)

    for file_path in file_list:
        print("***************************************************************************************************")
        print(file_path)

        # file_path = r"C:\Users\王衍升\Desktop\新建文件夹\1.txt"  # 替换为实际文件路径
        keyword_list = ['LWT']  # 替换为要提取的关键字列表
        window_size = 180 # 替换为要提取的关键字周围的字符数
        num_0 = 0
        data = extract_data_around_keyword(file_path, keyword_list, window_size)
        for item in data:
            print(item)
            if '"connected":"0"' in item:
                num_0+=1
            print("======================================")
        print("一共掉线{}次".format(num_0))

