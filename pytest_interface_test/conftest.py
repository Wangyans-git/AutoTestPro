#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 2024/5/21 17:35
# @Author  : yansheng.wang
# @File    : conftest.py.py
# @Description : 解决路径问题

import os

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))