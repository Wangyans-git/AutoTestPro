#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-

import time
import threading

# def worker():
#     print("Worker starting...")
#     time.sleep(5)
#     print("Worker done.")
#
# if __name__ == "__main__":
#     thread1 = threading.Thread(target=worker)
#     thread1.start()
#     print("Main thread waiting for worker to finish...")
#     thread1.join()
#     print("Main thread continues after worker finishes.")

import random

i = 1
a = random.randint(1, 9)
b = int(input("输入一个数字："))
print(a)
while a != b:
    if a > b:
        print("你输入的太小了")
        b = int(input("输入一个数字："))

    else:
        print("你输入的太大了")
        b = int(input("输入一个数字："))
