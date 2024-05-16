#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 2024/4/17 10:44
# @Author  : yansheng.wang
# @File    : filter_keywords.py
# @Description : 过滤关键字
import os
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # YOLOv5 root directory
file_path = str(Path(ROOT) / "解析数据")

file_list = os.listdir(file_path)

down = 0
up = 0

for i in file_list:
    with open(file_path + "/" + i, "r", encoding="utf-8") as file:
        # with open(f"原始数据\\{self.data_erp_sku}_{self.device_name}.txt", "w") as file:
        content = file.read()
        if "倒卧方式-> 立式" in content:
            up += 1
        elif "倒卧方式-> 卧式" in content:
            down += 1
print(f"立式{up}个")
print(f"卧式{down}个")


