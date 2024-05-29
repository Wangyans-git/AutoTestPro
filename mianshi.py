#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 2024/5/17 12:08
# @Author  : yansheng.wang
# @File    : mianshi.py
# @Description : 作用


# m = "asdfesdeedf"
# reversed_m = m[::-1]
# for i in reversed_m:
#     if i == "e":
#         pass
#     else:
#         print(i)
#
#
# m = [1, 1,7, 5, 3]
# k = 3
# k_min_num = sorted(m)[:k]
# print(k_min_num)


# m = [1, 1, 7, 5, 3]
# print(sorted(m)[::-1])
# print(list(set(m)))


# my_dict = {'a': 1, 'b': 2, 'c': 3}
# my_list = list(my_dict.items())
# print(my_list)


# my_list = (1, 2, 3, 4, 5)
# my_tuple = list(my_list)
# print(my_tuple)


#
# def is_valid_time(time_str, format_str):
#     try:
#         datetime.strptime(time_str, format_str)
#         return True
#     except ValueError:
#         return False
#
#
# while True:
#     user_input = input("输入时间：YYYY-MM-DD HH:MM:SS:")
#     print(user_input)
#     if is_valid_time(user_input, "%Y-%m-%d %H:%M:%S"):
#         print("时间格式正确")
#         break
#     else:
#         print("时间格式不正确")
#         # continue
# result = (0 << 16) + (0 << 8) + 5
# print(result)

def d():
    sku_info = {
        # "self.device": None,  # 设备devices
        # "self.sku": None,  # sku
        # "self.sku_type": None,  # 设备功能分类
        # "self.sku_instance": None,  # instance
        # "self.sku_value_enum": None,  # value
        # "self.sku_value_integer": None,  # value
        "self.services": "services",
        "self.test_sku": "sku",
    }
    return sku_info


print(d["self.test_sku"])
