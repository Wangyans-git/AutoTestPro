#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
@Time    : 2022/6/9 12:07
@Author  : jhcheng
@FileName: loger2.py
@SoftWare: PyCharm
"""
from loguru import logger
from H7131.myConfig import setting
import time


class Loger():
    def __init__(self, logfile_name):
        self.log_path = setting.LOG_DIR
        now = time.strftime("%Y-%m-%d %H-%M-%S")
        log_name_py = self.log_path + '/' + now + "_" + logfile_name + "_脚本日志.txt"
        log_name_com = self.log_path + '/' + now + "_" + logfile_name + "_串口日志.txt"

        logger.remove(handler_id=None)  # 清除之前的设置
        # 设置生成日志文件，utf-8编码，每天0点切割，zip压缩，保留3天，异步写入
        logger.add(sink=log_name_py, level='INFO', rotation='00:00', encoding='utf - 8', enqueue=True,
                   filter=lambda record: record["extra"]["name"] == "脚本_log")

        logger.add(sink=log_name_com, level='INFO', rotation='00:00', encoding='utf - 8', enqueue=True,
                   filter=lambda record: record["extra"]["name"] == "串口_log")

        # 这个bind()函数就是在extra里额外增加键值
        self.logger_py = logger.bind(name="脚本_log")
        self.logger_com = logger.bind(name="串口_log")

    def get_py_logger(self):
        return self.logger_py

    def get_com_logger(self):
        return self.logger_com


if __name__ == '__main__':
    name = '1111'
    Loger(name).get_py_logger()
