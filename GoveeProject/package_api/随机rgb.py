#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 作用

import random


def generate_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    hex_color = f"{red:02x}{green:02x}{blue:02x}"
    return hex_color


rgb_list = ''
for i in range(20):
    random_color = generate_random_color()
    rgb_list += random_color
print(rgb_list)
