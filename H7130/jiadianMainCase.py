#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
@Time    : 2022/11/9 15:57
@Author  : jhcheng
@FileName: jiadianMainCase.py
@SoftWare: PyCharm
"""
# from ui2Handle.jiadianHandle import JiaDianHandle
from H7130.ui2Handle.jiadianHandle import JiaDianHandle
import unittest


class JiaDianMainCase(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        # phone_name = '424e4d504c383098'
        phone_name = 'd5cd8968'  # 小米10
        device_name = ['Smart Heater' ]
        # device_name = ['Smart Heater', ]
        self.jiadian_handle = JiaDianHandle(phone_name, device_name[0])

    # 前置条件
    def setUp(self) -> None:
        print('开始测试')

    def test_jiadian_mode(self):
        # 测试次数
        times = 1000000
        try:
            self.jiadian_handle.jiadian_mode_switch(times)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(JiaDianMainCase("test_jiadian_mode"))
