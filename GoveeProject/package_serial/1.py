#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @Description : 单机压测

import random
import time
import schedule
import subprocess


# 生成随机的小时、分钟和秒
hour = random.randint(9, 9)
minute = random.randint(10, 25)
# second = random.randint(0, 59)

# 格式化为时间字符串
random_time = "{:02d}:{:02d}".format(hour, minute)
print(type(random_time))

t = "19:18"


def my_task():
    print("任务执行时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # 连接设备
    device = "R5CRC1V0GLW"

    # 打开手机电源键
    command = f"shell input keyevent {26}"
    adb_command = f"adb shell {command} on {device}"
    print(adb_command)
    subprocess.run(adb_command, shell=True, check=True)

# 创建一个调度器
scheduler = schedule.Scheduler()

# 定义任务执行时间
scheduler.every().day.at(t).do(my_task)

# 无限循环，直到任务执行
while True:
    scheduler.run_pending()
    time.sleep(1)
