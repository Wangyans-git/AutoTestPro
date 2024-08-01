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
import os
import time
from datetime import datetime

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

# 定义一个函数，用于子进程执行的任务
# def worker(num):
#     print(f'Worker {num} is working')
#
# if __name__ == '__main__':
#     # 创建多个子进程
#     processes = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i,))
#         processes.append(p)
#         p.start()
#     # 等待所有子进程结束
#     print("555")
#     for p in processes:
#         p.join()
#
#     print('All workers have finished')

# import random
# import string
#
#
# def generate_password(length=12):
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choice(characters) for i in range(length))
#
#
# password = generate_password()
# print(password)


# def concatenate_with_fstrings(n):
#     result = ''.join(f'{i}' for i in range(n))
#     return result
#
#
# start_time = time.time()
# concatenate_with_fstrings(100000)
# end_time = time.time()
# print(f"Using f-strings: {end_time - start_time} seconds")

# numbers = [3, 1, 4, 1, 5, 9, 2, 6]
# max_value = sorted(numbers)
# print(list(set(max_value)))


# s = "12345"
# is_all_digits = all(c.isdigit() for c in s)
# print(is_all_digits)

# my_string = "hello"
# unique_chars = sorted(my_string)
# print(unique_chars)
# def square(x):
#     return x + x


# numbers = [i for i in range(1, 10000)]
# iterator = iter(numbers)
# for i in iterator:
#     print(i)
# thekey.findit("oldA", "D:/AutoTestProjects")   # 全文搜索关键字


# my_dict = {'apple': 5, 'banana': 1, 'orange': 3}
# sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1]))
# print(sorted_dict)


# def capitalize_string(s):
#     return ' '.join(word.capitalize() for word in s.split())
#
# test_str = "hello python world"
# print(capitalize_string(test_str))


# def merge_dicts(dict1, dict2, dict3):
#     return dict1,dict2,dict3
#
#
# dict1 = {'a': 1, 'b': 2}
# dict2 = {'c': 3, 'd': 4}
# dict3 = {'e': 5, 'f': 6}
# print(merge_dicts(dict1, dict2, dict3))


# my_list = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
# count = Counter(my_list)
#
# print(count)


# import _thread
# import time
#
# def print_time(thread_name, delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print(f"{thread_name}: {time.ctime(time.time())}")
#
# try:
#     _thread.start_new_thread(print_time, ("Thread-1", 2))
#     _thread.start_new_thread(print_time, ("Thread-2", 4))
# except:
#     print("Error: unable to start thread")
#
# time.sleep(5)


# import wget
#
# def progress_bar(current, total, width=80):
#     progress = current / total
#     bar = '#' * int(progress * width)
#     percentage = round(progress * 100, 2)
#     print(f'[{bar:<{width}}] {percentage}%')
# url = 'http://s3.amazonaws.com/govee-public/upgrade-pack/8adad59e8e7bcc504c942bd2f2a1f545-H7137_WIFI_BLE_HW4.02.01_SW1.00.10_OTA.bin'
# save_path = '可惜没如果.mp3'
#
# wget.download(url, save_path, bar=progress_bar)


# import pyautogui
# screenshot = pyautogui.screenshot()
# screenshot.save('screenshot.png')

# import turtle
# t = turtle.Turtle()
# for i in range(100):
#     t.forward(i * 10)
#     t.right(90)
# turtle.done()


# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
# encrypted_text = cipher_suite.encrypt(b"A secret message.")
# print(encrypted_text)
# from skimage.metrics import structural_similarity as ssim
# def calculate():
#     try:
#         image2_path = f'crop_1.jpg'  # 正确图片
#         image1 = cv2.imread(f'111.jpg', cv2.IMREAD_GRAYSCALE)
#         image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
#         score, _ = ssim(image1, image2, full=True)
#         print(score)
#         # return score
#     except Exception as e:
#         print(e)
#
# calculate()

# image = cv2.imread('111.jpg')
# jpeg_quality = 80  # JPEG质量，0-100之间
# cv2.imwrite('output_image.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

# from datetime import datetime
# import pytz
#
# try:
#     date_str = input("请输入日期时间（格式为YYYY-MM-DD HH:MM:SS）: ")
#     naive_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
#     aware_datetime = pytz.timezone('Asia/Shanghai').localize(naive_datetime)
#     print("解析后的日期时间对象:", aware_datetime)
# except ValueError as e:
#     print("日期时间格式不正确:", e)

# import time
#
# import uiautomator2 as u2
#
# d = u2.connect_usb()
# d.implicitly_wait(30)
# # d.app_start('com.govee.home')
# on = d(text="已开启")
# off = d(text="已关闭")
# govee_on = d(resourceId='com.govee.home:id/iv_switch')
# govee_off = d(resourceId='com.govee.home:id/iv_switch')
# i = 0
# while True:
#     while i < 10:
#         if i < 5:
#             d.app_start('com.google.android.apps.chromecast.app', use_monkey=True)
#             on.click()
#             d.sleep(1.5)
#             off.click()
#             d.sleep(1.5)
#         else:
#             d.app_start('com.govee.home', use_monkey=True)
#             govee_on.click()
#             time.sleep(2)
#             govee_off.click()
#             time.sleep(2)
#         i += 1
#     i = 0

# lock = threading.Lock()
#
# def run1():
#     while 1:
#         print(1)
#
#
# def run2():
#     while 1:
#         print(2)
#
#
# threading.Thread(target=run1).start()
# threading.Thread(target=run2).start()


# import threading
#
# # 共享资源
# shared_counter = 0
# # lock = threading.Lock()
#
#
# def increment_counter():
#     global shared_counter
#     for _ in range(100):
# lock.acquire()
# try:
# shared_counter += 1
# finally:
#     lock.release()
#
#
# # 创建多个线程
# threads = []
# for _ in range(21):
#     t = threading.Thread(target=increment_counter)
#     threads.append(t)
#     t.start()
# # print(threads)
# # 等待所有线程完成
# for t in threads:
#     t.join()
#
# print("Final counter value:", shared_counter)

# # 为/否则
# for x in range(5):
#     print(x)
# else:
#     print("Loop Completed")  # 执行# While / Else
# i = 0
# while i < 5:
#     i+=1
# else:
#     print("Loop Completed")  # 未执行


# def func(*args, **kwargs):
#     print(*args, **kwargs)
#
#
# list_1 = [100, 200]
# dict_1 = {'x': 300, 'y': 400}
# func(list_1)
# func(dict_1)

# 彬哥，我个人原因决定还是要回武汉发展了，这两年感谢彬哥给予我机会和支持，也感谢公司提供的平台让我成长
# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#
#     return wrapper
#
#
# @my_decorator
# def say_hello() -> None:
#     print("Hello!")
#
#
# say_hello()

# import sys
#
# from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
#
#
# class Worker(QObject):
#     finished = pyqtSignal()
#
#     def __init__(self):
#         super().__init__()
#         self.is_paused = False
#
#     @pyqtSlot()
#     def run(self):
#         while True:
#             if not self.is_paused:
#                 print("Running...")
#                 self.start()
#
#             else:
#                 print("Paused...")
#             QThread.msleep(1000)  # 模拟耗时操作，每次暂停1秒
#
#     def pause(self):
#         self.is_paused = True
#
#     def resume(self):
#         self.is_paused = False
#
#     def start(self):
#         print("111")
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.worker = Worker()
#         self.thread = QThread()
#         self.worker.moveToThread(self.thread)
#         self.thread.started.connect(self.worker.run)
#         self.worker.finished.connect(self.thread.quit)
#         self.worker.finished.connect(self.worker.deleteLater)
#         self.thread.finished.connect(self.thread.deleteLater)
#         self.thread.start()
#
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle("Pause and Resume Example")
#         self.setGeometry(100, 100, 400, 300)
#
#         self.pause_button = QPushButton('Pause', self)
#         self.pause_button.setGeometry(50, 50, 100, 50)
#         self.pause_button.clicked.connect(self.pauseClicked)
#
#         self.resume_button = QPushButton('Resume', self)
#         self.resume_button.setGeometry(200, 50, 100, 50)
#         self.resume_button.clicked.connect(self.resumeClicked)
#
#     def pauseClicked(self):
#         self.worker.pause()
#         print("Paused the worker.")
#
#     def resumeClicked(self):
#         self.worker.resume()
#         print("Resumed the worker.")
#
#     def closeEvent(self, event):
#         self.worker.finished.emit()
#         self.thread.quit()
#         self.thread.wait()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = MainWindow()
#     mainWindow.show()
#     sys.exit(app.exec_())


raw_num = int('4' + '2' +'4' + '7', 16)
print(raw_num)
