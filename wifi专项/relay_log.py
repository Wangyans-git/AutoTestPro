import datetime
import random
import re
import time

import serial
from loguru import logger


class Relay:

    def __init__(self, port_number, band_rate):
        self.port_number = port_number
        self.band_rate = band_rate

    def open_relay(self):
        self.relay_serial = serial.Serial(self.port_number, self.band_rate)
        return self.relay_serial

    def turn_on(self):
        logger.info("开")
        self.relay_serial.write(bytes.fromhex('A0 01 01 A2'))

    def turn_off(self):
        logger.info("关")
        self.relay_serial.write(bytes.fromhex('A0 01 00 A1'))


class Device:
    def __init__(self, port_number, band_rate, keyword, keyword2, keyword3, keyword4):
        self.port_number = port_number
        self.band_rate = band_rate
        self.keyword = keyword
        self.keyword2 = keyword2
        self.keyword3 = keyword3
        self.keyword4 = keyword4

    def open_devicelog(self):  # 打开设备串口

        self.prot_serial = serial.Serial(self.port_number, self.band_rate)

    def write_pw(self):
        logger.info("输入指令iHoment_20170201")
        self.prot_serial.write(b'iHoment_20170201\n')

    def read_flash(self):
        logger.info("输入指令dev_info flash read 16220160 156")
        self.prot_serial.write(b'dev_info flash read 16220160 156\n')

    def console_name(self):
        now = datetime.datetime.now()
        self.consolename = now.strftime("%Y%m%d_%H%M%S") + ".txt"
        return self.consolename

    def console_log(self):
        logger.add(self.consolename, rotation="500MB")

    def file_name(self):
        now = datetime.datetime.now()
        self.filename = now.strftime("%Y%m%d_%H%M%S") + ".log"
        return self.filename

    def read_log(self):
        data = self.prot_serial.readline()  # 读取数据
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')  # 正则表达式匹配 ANSI 转义序列
        try:
            data = data.decode('utf-8').strip()  # 尝试将数据解码为 utf-8 编码格式
            data = ansi_escape.sub('', data)  # 去掉 ANSI 转义序列
        except UnicodeDecodeError:
            pass
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f')[:-3]  # 获取当前时间戳，并格式化为字符串
        self.line = '[{}] {}\n'.format(now, data)  # 将时间戳和数据拼接成一行
        with open(self.filename, "a") as f:
            f.write(self.line)
        return self.line

    def perform_operation(self):
        logger.info("超过1分钟没扫描到关键字")
        r.turn_off()
        logger.info("断电10秒")
        time.sleep(10)
        r.turn_on()
        logger.info("上电")

    def run(self):
        count = 0
        start_times = 0
        end_times = 0

        while True:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                d.read_log()
                if keyword2 in self.line:
                    line2 = self.line
                    logger.info("line2:{}".format(line2))
                    d.write_pw()
                    d.read_flash()
                    break
                elif keyword3 in self.line:
                    line3 = self.line
                    logger.info("line3:{}".format(line3))
                    d.write_pw()
                    d.read_flash()
                    break
                elif keyword4 in self.line:
                    line4 = self.line
                    logger.info("line4:{}".format(line4))
                    d.write_pw()
                    d.read_flash()
                    break
                elif elapsed_time > 60:
                    break

            while True:
                elapse_time = time.time() - start_time
                d.read_log()
                delayed_time = random.uniform(0.5, 1)
                if keyword in self.line:
                    count += 1
                    line1 = self.line
                    logger.info("line1:{}".format(line1))
                    time.sleep(delayed_time)
                    logger.info("延时{}秒断电".format(delayed_time))
                    r.turn_off()
                    logger.info("第{}次跑断电".format(count))
                    logger.info("断电10秒")
                    time.sleep(10)
                    r.turn_on()
                    break
                elif elapse_time > 60:
                    d.perform_operation()
                    break


if __name__ == '__main__':
    keyword = "[HAL_Flash_WriteData] flash_addr: 0xf7c000"
    keyword2 = "http client connect success"
    keyword3 = "subscribe success"
    keyword4 = "mqtt_service_subscribe_topic"

    r = Relay("com16", 9600)
    r.open_relay()
    r.turn_off()
    time.sleep(5)
    r.turn_on()
    d = Device("com3", 115200, keyword, keyword2, keyword3, keyword4)
    d.console_name()
    d.console_log()
    d.open_devicelog()
    d.file_name()

    d.run()
