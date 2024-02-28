import serial
import serial.tools.list_ports
import time
import random
import struct

from H7142.get_log.get_log import GetLog

SERIAL_COM = 'COM8'
SERIAL_BAUND = 19200
SERIAL_CMS_HEAD = 0x55
COM_INTERVAL = 0.6

LOG_FILE_NAME = "CMS-"

CMS_PROTOCOL_MAX_LEN = 6


def Serial_ComList():
    ports_list = list(serial.tools.list_ports.comports())
    print("ports_lsit:", ports_list)
    if len(ports_list) <= 0:
        print("无串口设备。")
    else:
        print("可用的串口设备如下：")
        for comport in ports_list:
            print(list(comport)[0], list(comport)[1])  # 串口信息


# 日志文件
class log_ops:
    def __init__(self):
        ts = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        try:
            self.logfile = open(LOG_FILE_NAME + str(ts) + ".log", mode='r', encoding='utf-8')
        except FileNotFoundError:
            print("create log file " + LOG_FILE_NAME + str(ts) + ".txt")
            self.logfile = open(LOG_FILE_NAME + str(ts) + ".log", mode='w+', encoding='utf-8')
            self.write_TimeStamp_Line(" ----------- Start ----------- ")

    def __del__(self):
        try:
            self.logfile.close()
        except Exception as err_info:
            print(err_info)

    def write_Line(self, data):
        self.logfile.write(data)
        self.logfile.write("\n")

    def write_TimeStamp_Line(self, data):
        ts = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        self.logfile.write(ts + ':' + data)
        self.logfile.write("\n")

    def write_EndMsg(self, data):
        self.write_TimeStamp_Line(" ----------- End " + data + " ----------- ")


"""
串口收发数据
"""


class serial_ops:
    def __init__(self, com=SERIAL_COM, baund=SERIAL_BAUND):  # 串口号，比特率
        self.com = com  # 串口号
        self.baund = baund  # 比特率
        print(str(self.com) + '\r')
        print("baund:" + str(self.baund) + '\r')
        self.serial_open()

    def __del__(self):
        self.serial_close()

    def serial_open(self):
        try:
            self.ser = serial.Serial(self.com, self.baund)
            print("Open {COM} Success ...".format(COM=self.com))
        except:
            print("Open {COM} Fail !!!.".format(COM=self.com))

    def serial_write_a(self, packet):
        try:
            self.ser.write(packet)
        except:
            print("WriteArry_a {COM} Fail !!!.".format(COM=self.com))

    def serial_write_str(self, packet):
        # print("输入:", packet)
        try:
            self.ser.write(packet)
            # print("执行了")
        except:
            print("WriteArry_str {COM} Fail !!!.".format(COM=self.com))

    def serial_write(self, data):
        try:
            packet = bytearray()
            packet.append(data)
            self.ser.write(packet)
        except:
            print("Write {COM} Fail !!!.".format(COM=self.com))

    def serial_read(self, data):
        try:
            data = self.ser.read.hex()
            print("read:", data)
        except:
            print("Read {COM} Fail !!!.".format(COM=self.com))

    def serial_close(self):
        try:
            self.ser.close()
            print("Close {COM} ...".format(COM=self.com))
        except:
            print("Close {COM} Fail !!!.".format(COM=self.com))


"""基础协议完善"""


class cms_com():
    def com_chk(self, packet):
        sum = 0
        it = iter(bytearray(packet))
        for x in it:
            sum += x
        sum &= 0xFF
        return sum

    # 格式化协议数据，返回指令给cms_range_test
    def com_normal_ops(self, com, list):
        packet = bytearray()
        packet.append(SERIAL_CMS_HEAD)  # 固定开头0x55
        packet.append(com)  # 遍历com，不同功能
        for data in list:
            packet.append(data)
        packet.append(self.com_chk(packet))  # 将完整数据添加到数组
        print("\n发送hex：", packet.hex())
        print("发送byte：", packet)
        return packet

    # 心跳
    def com_heartbeat_ops(self, beat=0x00):
        list = []
        list.append(beat)
        return self.com_normal_ops(0xF0, list)

    # 状态查询
    def com_devsta_ops(self, data):
        list = []
        list.append(data)
        return self.com_normal_ops(0xF1, list)

    # wifi
    def com_wifiset_ops(self, sta=0x00):
        list = []
        list.append(sta)
        return self.com_normal_ops(0xF3, list)

    # 绑定
    def com_bind_ops(self, sta=0x00):
        list = []
        list.append(sta)
        return self.com_normal_ops(0xF4, list)

    # 恢复出厂
    def com_factory_ops(self, sta=0x00):
        list = []
        list.append(sta)
        return self.com_normal_ops(0xF6, list)

    # 获取mcu软硬件版本号
    def com_verchk_ops(self, sta=0x00):
        list = []
        list.append(sta)
        return self.com_normal_ops(0xF7, list)

    # 开关
    def com_switch_ops(self, sta=0x00):
        list = []
        list.append(sta)
        return self.com_normal_ops(0x01, list)

    # 故障报警
    def com_mode_ops(self, sta=0x00):
        list = []
        list.append(sta)
        return self.com_normal_ops(0x02, list)

    # 熄屏
    def com_display_ops(self, sta=0x00):
        list = []
        list.append(sta)
        return self.com_normal_ops(0x07, list)

    # 0x55 19 01 01  档位
    def com_set_pra_ops(self, sta=0x01, para=0x01):
        list = []
        list.append(sta)
        list.append(para)
        return self.com_normal_ops(0x19, list)


"""基础协议完善"""


class iot_test_com():
    def H7142_Humi_Sync_Test(self, range):
        str_com = "iot_test -humi "
        str_com += str(hex(range))
        str_com += "\r"
        str_com += "\n"
        print(str_com)
        return str_com


"""
测试接口
"""


class cms_com_test(serial_ops, log_ops):
    send_times = 0
    recv_times = 0
    log = log_ops()

    def cms_sleep_time(self, interval=COM_INTERVAL):
        time.sleep(interval)
        count = self.ser.inWaiting()
        print("count:{}".format(count))  # 串口缓存大小
        if count > 0:
            rec_str = self.ser.read(count)
            print("-------------返回：{}-------------".format(rec_str.hex()) + "\n")
            if (count > CMS_PROTOCOL_MAX_LEN):
                self.recv_times = self.recv_times + 2
                # print("recv_times:",self.recv_times)
            else:
                self.recv_times = self.recv_times + 1
                # print("recv_times:", self.recv_times)
            self.log.write_TimeStamp_Line('Recv: ' + '[' + str(self.recv_times) + ']' + rec_str.hex())

    # 范围测试（输入范围内数据）
    def cms_range_test(self, packet_ops, A=0, B=0xFF):
        cnt = A
        exit = 0
        while (exit == 0):
            if (B <= 255):
                cnt = cnt & 0xFF  # 二进制位运算，如果都为1则为 1
                self.send_times = self.send_times + 1
                # self.log.write_TimeStamp_Line('send: '+'['+str(self.send_times)+']' + packet.hex())
                self.serial_write_str(packet_ops(cnt))
                # print("调试：", packet_ops(cnt))
                cnt = cnt + 1
            elif (B <= 65535):
                com = cnt >> 8  # 把">>"左边的运算数的各二进位全部右移若干位，">>"右边的数指定移动的位数
                para = cnt & 0xFF
                packet = packet_ops(com, para)
                self.send_times = self.send_times + 1
                self.log.write_TimeStamp_Line('send: ' + '[' + str(self.send_times) + ']' + packet.hex())
                self.serial_write_a(packet_ops(com, para))
                cnt = cnt + 1
            else:
                pass
            self.cms_sleep_time()
            if (cnt > B):
                exit = 1
                self.log.write_TimeStamp_Line('ALL Send [%d]' % self.send_times)
                self.log.write_TimeStamp_Line('ALL Recv [%d]' % self.recv_times)
                self.send_times = 0
                self.recv_times = 0
                self.log.write_EndMsg(packet_ops.__name__)

    # 错误测试
    def cms_err_test(self, packet_ops, err_ops, A=0, B=0xFF):  # 255
        cnt = A
        exit = 0
        while (exit == 0):
            if (B <= 255):
                cnt = cnt & 0xFF
                packet = packet_ops(cnt)
                packet = err_ops(packet)
                self.log.write_TimeStamp_Line('send err: ' + packet.hex())
                self.serial_write_a(packet)
                cnt = cnt + 1
            elif (B <= 65535):
                com = cnt >> 8
                para = cnt & 0xFF
                packet = packet_ops(com, para)
                packet = err_ops(packet)
                self.log.write_TimeStamp_Line('send err: ' + packet.hex())
                self.serial_write_a(packet)
                cnt = cnt + 1
            else:
                pass
            if (cnt > B):
                exit = 1
                self.log.write_EndMsg(self.__class__.__name__)
            self.cms_sleep_time()


"""
测试类型
"""


class cms_err_type():
    # 校验和错误
    def cms_err_TypeChk(self, package):
        package[-1] = random.randint(0, 0xFF)
        return package

    # 正常数据 + 部分异常数据
    def cms_err_ComWithErr(self, package, len):
        for i in range(len):
            package.append(random.randint(0, 0xFF))
        return package

    #  部分异常数据 + 正常数据
    def cms_err_ErrWithCom(self, package, len):
        for i in range(len):
            package.insert(0, random.randint(0, 0xFF))
        return package

    # #  随机数据
    # def cms_err_RandomData(self, package):
    #     len = random.randint(1, 10)
    #     err_data = bytearray()
    #     for i in range(len):
    #         err_data.append(random.randint(0, 0xFF))
    #     print("错误数据：",err_data)
    #     return err_data

    # #  部分正常加正常数据
    def cms_err_RandomData(self, package):
        package_len = len(package)
        for i in range(package_len):
            package.append(package[i])
        random_len = random.randint(1, 3)
        index = 0
        for i in range(random_len):
            package.pop(2 + i - index)
            index = index + 1
        return package

    def cms_err_ComWithErrRandom(self, package):
        rannum = random.randint(0, 5)
        return self.cms_err_ComWithErr(package, rannum)

    def cms_err_RandomErrWithCom(self, package):
        rannum = random.randint(0, 5)
        return self.cms_err_ErrWithCom(package, rannum)


def Run():
    cms_protocol = cms_com()  # 实例化基础协议类
    cms_test = cms_com_test()  # 实例化测试接口类
    err_type = cms_err_type()  # 压测类型类（错误数据，随机数据）
    iot_test = iot_test_com()  # iot测试类

    """   # 0x55 19 01 01
    def com_set_pra_ops(self, sta=0x01, para=0x01):
        list = []
        list.append(sta)
        list.append(para)
        return self.com_normal_ops(0x19, list)"""
    while True:
        # cms_test.cms_range_test(cms_protocol.com_set_pra_ops)  # 档位
        cms_test.cms_range_test(cms_protocol.com_display_ops)  # 熄屏
        cms_test.cms_range_test(cms_protocol.com_switch_ops)  # 开关
        cms_test.cms_range_test(cms_protocol.com_verchk_ops)  # 获取版本号
        cms_test.cms_range_test(cms_protocol.com_devsta_ops)  # 状态查询
        # cms_test.cms_range_test(cms_protocol.com_heartbeat_ops)  # 心跳
        # cms_test.cms_err_test(cms_protocol.com_heartbeat_ops,err_type.cms_err_RandomData,0,100)
        # cms_test.cms_range_test(iot_test.H7142_Humi_Sync_Test, 0, 101)


if __name__ == '__main__':
    Serial_ComList()
    Run()
