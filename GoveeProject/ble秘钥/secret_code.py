#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :yansheng.wang
# @File    :
# @Description : 小家电API
import requests

def generic_methods():
    url = " https://app2.govee.com/device/rest/devices/v1/bind"
    headers = {
        'clientType': '1',
        'Accept-Language': 'zh',
        'appVersion': '5.8.10',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImFjY291bnQiOiJ7XCJjbGllbnRcIjpcIjNhMzU0MmJlYTk0ZDQ4Y2JhZmM3MzA0ZmEzZmJjYjdlXCIsXCJzaWRcIjpcImg3N2NVQWs2YnhRQktjckQ1azZrZGVWbU45VkpkY28xXCIsXCJhY2NvdW50SWRcIjo0NDY0MjU1LFwiZW1haWxcIjpcIjE5NjM4MDY5NjJAcXEuY29tXCJ9In0sImlhdCI6MTY5NTI2NDM4MywiZXhwIjoxNzAwNDQ4MzgzfQ.CkilRclASZX-ZHfK4X5gWQECU3-G56ydu6S_e7BLR4I',
        'timezone': 'Asia/shanghai',
        'clientId': '3a3542bea94d48cbafc7304fa3fbcb7e',
        'timestamp': '165768516800',
        'X-RateLimit-Remaining': '91',
        'X-RateLimit-Reset': '1693298648',
        'X-RateLimit-Limit': '100',
        'x-api-key': 'm20xwttRNzBIKE8KP8wP5Mz7S61aSFa8x9cYOTU9',
        'sysVersion': '16.6.1',
        'envId': '0',
        'iotVersion': '0',
        'country': 'CN',
        'Content-Type': 'application/json'
    }

    payload =  {
    "deviceExt":"{\n  \"address\" : \"D4:AD:FC:5B:47:67\",\n  \"pactCode\" : 1,\n  \"autoShutDownOnOff\" : 0,\n  \"mcuHardVersion\" : \"23.01.02\",\n  \"wifiMac\" : \"D4:AD:FC:5B:47:66\",\n  \"deviceName\" : \"Smart Heater\",\n  \"pactType\" : 1,\n  \"mcuSoftVersion\" : \"23.01.01\",\n  \"secretCode\" : \"t9RpEEHm+ts=\",\n  \"dumpOnOff\" : 1,\n  \"bleName\" : \"ihoment_H7130_4767\"\n}",
    "timestamp":"1695264626198",
    "device":"7E:69:D4:AD:FC:5B:47:66",
    "value":"hwba7u62d3k6ydt42b892459462ff2943c90bac53b322137a6f3539152dcb00f2a4ac6960305659f",
    "versionSoft":"1.00.33",
    "sku":"H7130",
    "versionHard":"1.02.00",
    "pointsAdded":0
}

    response = requests.request("POST", url, headers=headers, json=payload)

    print(response.text.encode())

generic_methods()