import base64
import datetime
import json
import re
import time

import chardet

SKU = "H7143"
Version = "v1.0"

LOG_FILE_NAME = "in_log.txt"
DECODE_FILE_NAME = "out_log.txt"
USER_TIMEZONE = 8
# This website could query the location of timezone all around the world
# https://www.zeitverschiebung.net/cn/
# New York City 5
# Los Angeles   8

# from START -----------------------------------------------------
# "u": "安卓(app4.2及以上)",
# "v": "苹果(app4.2及以上)",
# "x": "安卓status查询消息（app4.2及以上）",
# "y": "苹果status查询消息（app4.2及以上）",
# "f": "alexa",
# "g": "google",
# "h": "ifttt",
# "i": "昼夜节律,联动（未来这俩种也会区分开）",
# "1": "govee定时开关",
# "o": "开放api",
# "s": "siri",
# "e": "测服自动化压测",
# "c": "govee home云端特殊控制（H5151）",
# "no": "其它(可能旧app（包括查询消息）响应，旧版本设备的本地与蓝牙控制，和上线后的status消息)",
# "old": "部分旧设备旧固件上报(写死的transaction)",
# "Govee": "部分旧设备旧固件上报(Govee开头的transaction)",
# "oldA": "[~]物理断电上电控制次数（如果有旧版本，就还包括旧设备的'[~]设备本地控制...+ iot重连上报消息'）",
# "a": "[~]设备本地控制（蓝牙或物理）+ 设备网络不稳定iot重连后也会上报该消息（未来新通用固件计划把这部分过滤掉）",
# "k": "ios小组件",
# "j": "联动",
From_Key_Tup = ('u', 'v', 'x', 'y', 'f', 'g', 'i', 'h', 's', 'oldA', 'a', 'j')
From_KeyName_Tup = (
    'android',
    'iphone',
    'android status',
    'iphone status',
    'alexa',
    'google',
    'diel rhythm',
    'ifttt',
    'siri',
    'poweron',
    'device',
    'linkage',
    'other',)
# from END -----------------------------------------------------


# BLE START -----------------------------------------------------
# 在 HEX 和 MEANING 按顺序填入对应的指令
BLE_Protocol_HEX = (
    '0x11',
    '0x12',
    '0x13',
)

BLE_Protocol_MEANING = (
    '延时关机',
    '定时组',
    '定时器'
)

BLE_Special_Protocol_HEX = (
    '0x05',
    '0x10',
    '0x17',
    '0x19',
    '0x1F',
    '0x22',
    '0x23',
    '0x16',
    '0x08',
    '0x1B',
)

BLE_Special_Protocol_MEANING = (
    '模式',
    '当前温度',
    '异常',
    '当前状态',
    '开关类',
    '保温设置',
    '预约模式',
    '显示',
    '绑定子设备',
    '氛围灯',
)
# 运行时，会自动添加
BLE_Protocol = {
}
BLE_Special_Protocol = {
}


# BLE END -----------------------------------------------------

# class Mqtt_Utils START --------------------------------------
class Mqtt_Utils:
    log_dict = {}
    log_json = []

    # LOG_FILE_NAME is the MQTT log that comes from the user's device.
    # DECODE_FILE_NAME is the data that after parsed
    def __init__(self):
        try:
            # 尝试获取文本的编码格式
            file = open(LOG_FILE_NAME, 'rb')
            encodingType = chardet.detect(file.read())['encoding']
            file.close()

            self.in_file = open(LOG_FILE_NAME, mode='r', encoding=encodingType)
            self.out_file = open(DECODE_FILE_NAME, mode='w', encoding='utf-8')
        except FileNotFoundError:
            print("create input file " + LOG_FILE_NAME)
            self.in_file = open(LOG_FILE_NAME, mode='w+', encoding='utf-8')

    def __del__(self):
        try:
            self.in_file.close()
            self.out_file.close()
        except Exception as err_info:
            print(err_info)

    # 输出到文件
    def output_to_file(self, data):
        self.out_file.write(data)
        self.out_file.write("\n")

    # hex 输出
    @staticmethod
    def format_hex(data):
        output_str = ""
        for byte_data in data:
            output_str += ("{:02x} ".format(byte_data))
        return output_str

    #
    def insert_str(self, source_str, insert_str, pos):
        return source_str[:pos] + insert_str + source_str[pos:]

    # mac 地址预处理
    def format_mac(self, in_str):
        # 处理mac地址格式，后面好做解析
        mac_addr = re.search(r'([a-f0-9]{2}:){7}[a-f0-9]{2}', in_str, re.I)
        if None != mac_addr:
            new_str = self.insert_str(in_str, '\"', mac_addr.span()[0])
            new_str = self.insert_str(new_str, '\"', mac_addr.span()[1] + 1)
            return new_str
        else:
            return in_str

    #
    def split_log(self, f_line, f_head, f_tail):
        s_head = f_line.find(f_head)
        s_tail = f_line.find(f_tail)
        if (s_head == -1) or (s_tail == -1):
            return -1
        else:
            s_head = re.split(f_head, f_line)
            s_tail = re.split(f_tail, s_head[1])
            return s_tail[0]

    def remove_log(self, in_str, range_red, range_green):
        range_r = in_str.find(range_red)
        range_g = in_str.find(range_green)
        if (range_r != -1) and (range_g != -1):
            return in_str[:range_r] + in_str[range_g:]
        else:
            return None

    def renew_log(self, str_info):
        list1 = []
        str_info = str_info.replace('{', ' ')
        str_info = str_info.replace('}', ' ')
        str_info = str_info.split('\",')
        for l in str_info:
            b = []
            a = l.strip().split('\":')
            for i in a:
                b.append(i.strip("\""))
            list1.append(b)

        for d in list1:
            self.log_dict[d[0]] = d[1]


# class General_BLE START --------------------------------------
# 通用 BLE 协议
class General_BLE:
    def general_delayclose_count(self, cmd, data):

        if (data[2] == 0x01):
            info = "开启 "
        else:
            info = "关闭 "
        info = info + "{:0>2d}".format(data[3]) + ':' + "{:0>2d}".format(data[4])
        return str(BLE_Protocol[cmd]) + '-> ' + info

    def general_timer_count(self, cmd, data):
        return str(BLE_Protocol[cmd]) + '-> ' + str(data)

    def general_timer_prase(self, cmd, data):
        info = ""
        index = str(data[2] + 1)
        if (data[3] & 0x80):
            info += "定时有效 "
        else:
            info += "定时无效 "
        if (data[3] & 0x01):
            info += "开机 "
        else:
            info += "关机 "
        info += "{:0>2d}".format(data[4]) + ':' + "{:0>2d}".format(data[5])
        if (data[6] & 0x80 != 0x00):
            info += " 不重复 "
        elif (data[6] & 0x7F != 0x00):
            info += " 重复时间 " + str(bin(data[6]))
        else:
            info += " 每天重复 "
        info += "模式-" + data[7:10].hex()
        return str(BLE_Protocol[cmd]) + str(index) + '-> ' + info


# class Special_BLE START --------------------------------------
# SKU 特有协议解析
class Special_BLE:
    def Special_BLE_Mode_prase(self, cmd, data):
        info = ""
        cmd_type = data[2]
        mode = data[3]
        if cmd_type == 0x00:
            info += "当前模式: "
            if mode == 0x01:
                info += "手动档"
            elif mode == 0x02:
                info += "DIY模式"
            elif mode == 0x03:
                info += "自动模式"
            else:
                info += "错误模式"
        elif cmd_type == 0x01:
            shift = data[3]
            info += "手动档参数 {:d}".format(shift)
        elif cmd_type == 0x02:
            run_index = data[3] & 0x0F
            info += "DIY参数 运行组 {:d} \n".format(run_index)
            set_shift = data[4]
            set_time = data[5] << 8 | data[6]
            left_time = data[7] << 8 | data[8]
            info += "组{:d} 挡位{:d} 设置时间{:d} 剩余时间{:d}\n".format(0, set_shift, set_time, left_time)
            set_shift = data[9]
            set_time = data[10] << 8 | data[11]
            left_time = data[12] << 8 | data[13]
            info += "组{:d} 挡位{:d} 设置时间{:d} 剩余时间{:d}\n".format(1, set_shift, set_time, left_time)
            set_shift = data[14]
            set_time = data[15] << 8 | data[16]
            left_time = data[17] << 8 | data[18]
            info += "组{:d} 挡位{:d} 设置时间{:d} 剩余时间{:d}".format(2, set_shift, set_time, left_time)
        elif cmd_type == 0x03:
            on = (data[3] & 0x80) >> 7
            targer = (data[3] & 0x7F)
            info += "自动档参数 自动停止{:d} 目标湿度{:d}".format(on, targer)
            info += "舒适模式 {:d}".format(data[4])
        else:
            info += "错误模式"
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info
    
    def Special_BLE_Display_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x01):
            if (data[3] == 0xff and data[4] == 0xff and data[5] == 0xff and data[6] == 0xff):
                info += "永久打开 "
            else:
                info += "时间段打开 "
                info += "{:0>2d}".format(data[3]) + ':' + "{:0>2d}".format(data[4])
                info += " to "
                info += "{:0>2d}".format(data[5]) + ':' + "{:0>2d}".format(data[6])
        elif (data[2] == 0x00):
            info += "永久关闭 "
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_SlaveDevice_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x00 and data[3] == 0x00):
            info += "无 "
        else:
            info += "子设备 {:x}:{:x}:{:x}:{:x}:{:x}:{:x}".format(data[2], data[3], data[4], data[5], data[6], data[7])
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_NightLight_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x01): #开关亮度
            if (data[3] == 0x01):
                info += "开 "
                info += "亮度{:d} ".format(data[4])
            else:
                info += "关 "
                info += "亮度{:d} ".format(data[4])
        elif (data[2] == 0x05):#模式
            if (data[3] == 0x0d):
                info += "颜色模式 "
            elif (data[3] == 0x13):
                info += "场景模式 "
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_SensorData_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x01):
            info += "sensor在线 "
        else:
            info += "sensor离线 "
        temp = (data[3] << 16) + (data[4] << 8) + data[5]
        humi = temp % 1000
        temper = (temp - humi) / 1000
        info += "当前湿度 {:f}".format(humi / 10)
        info += " 当前温度 {:f}".format(temper / 10)
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_Abnormal_prase(self, cmd, data):
        info = ""
        clean = data[2]
        sta = data[3]
        warn = data[4]
        if clean == 1:
            info += "需要清洁 "
        if sta == 1:
            info += "自动待机 "
        if warn == 1:
            info += "缺水提醒 " 
        elif warn == 2:
            info += "NTC保护 "
        elif warn == 4:
            info += "干烧保护 "
        elif warn == 8:
            info += "NTC失效 "
        elif warn == 16:
            info += "PTC失效 "
        elif warn == 32:
            info += "水箱提起 "  
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_State_prase(self, cmd, data):

        info = ""
        sta = data[2]
        if sta == 0:
            info += "空闲 "
        elif sta == 1:
            info += "加热 "
        elif sta == 2:
            info += "保温 "
        elif sta == 3:
            info += "煮沸 "
        elif sta == 4:
            info += "到达目标温度 "
        elif sta == 5:
            info += "冷却中 "
        elif sta == 6:
            info += "预约中 "
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_Switch_prase(self, cmd, data):
        info = ""
        # cmd_type = data[2]
        # if cmd_type == 6:
        #     info += "蜂鸣器开关 {:d}".format(data[4])
        info += "童锁 {:d}".format(data[2])
        info += "热雾 {:d}".format(data[4])
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_KeepWarm_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x01):
            info = info + "设备保温打开 "
        elif (data[2] == 0x00):
            info = info + "设备保温关闭 "
        time = int(str(data[3]) + str(data[4]))
        info += "保温设定{:d}分钟 ".format(time)
        info += "保温剩余{:d}分钟 ".format(data[5])
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_Reserve_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x00):
            info = "预约开关为："
            info = info + "关 "
        elif (data[2] == 0x01):
            info = info + "开 "
        info = info + "预约开始工作的时间为{:d}min后: ".format((data[3] << 8 | data[4]))
        timestamp = int(data[5] << 24 | data[6] << 16 | data[7] << 8 | data[8])
        info = info + "当前预约时间戳（有效值仅为时分，日期为默认值）：" + str(datetime.datetime.fromtimestamp(timestamp))
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_xxx_prase(self, data):
        return "Special_BLE_xxx_prase"


# class Mqtt_Prase START --------------------------------------
class Mqtt_Prase:
    utils = Mqtt_Utils()
    ble_decode = General_BLE()
    ble_specail = Special_BLE()
    LWT_Count = 0
    From_KeyCount_List = [0] * (len(From_KeyName_Tup))
    Line_FromMSG = "from:"

    def prase_ble_protocol_init(self):
        for i in range(len(BLE_Protocol_HEX)):
            BLE_Protocol[BLE_Protocol_HEX[i]] = BLE_Protocol_MEANING[i]
        print(BLE_Protocol)

        for i in range(len(BLE_Special_Protocol_HEX)):
            BLE_Special_Protocol[BLE_Special_Protocol_HEX[i]] = BLE_Special_Protocol_MEANING[i]
        print(BLE_Special_Protocol)

    def prase_general_info(self, i_head, i_info):
        self.utils.output_to_file(str(i_head) + str(i_info))

    def prase_stc_info(self, i_info):
        if '_' in i_info:
            info = re.split('_', i_info)
            op = info[0]
            boot = info[1]
            rssi = info[2]
            run = info[3]

            stc = "op: " + op
            if (boot == '0'):
                stc = stc + " ,boot : 断电上电"
            elif (boot == '1'):
                stc = stc + " ,boot : 主动重启"
            else:
                stc = stc + " ,boot : 异常，需注意！！！！！"
            stc = stc + " , RSSI: " + rssi
            stc = stc + " , Running: " + run
            self.utils.output_to_file("stc: " + stc)

    def prase_status_info(self, i_info):
        if "onOff" in i_info:
            self.utils.output_to_file("onoff:" + str(i_info["onOff"]))
        if "sta" in i_info:
            self.utils.output_to_file("sta:" + str(i_info["sta"]))
            if "stc" in i_info["sta"]:
                self.prase_stc_info(i_info["sta"]["stc"])

    def prase_timestamp_info(self, timestamp):
        self.utils.output_to_file('UTC:  ' + str(timestamp))
        self.utils.output_to_file('User_TimeZone:' + str(USER_TIMEZONE))
        self.utils.output_to_file('China:' + str(datetime.datetime.fromtimestamp(timestamp / 1000)))
        self.utils.output_to_file(
            'User:' + str(datetime.datetime.fromtimestamp((timestamp / 1000) + (-USER_TIMEZONE - 8) * 3600)))
        self.utils.output_to_file('----------------------------\r')

    def prase_BLE_decode(self, info):
        for i in info:
            base64_data = base64.b64decode(i)
            self.prase_general_info("", self.utils.format_hex(base64_data))
            cmd = '0x{:>02X}'.format(base64_data[1])
            if (cmd in BLE_Protocol):
                if (cmd == "0x12"):
                    rst = self.ble_decode.general_timer_count(cmd, base64_data[2])
                elif (cmd == "0x13"):
                    rst = self.ble_decode.general_timer_prase(cmd, base64_data)
                elif (cmd == "0x11"):
                    rst = self.ble_decode.general_delayclose_count(cmd, base64_data)
                self.utils.output_to_file(rst)

            if (cmd in BLE_Special_Protocol):
                if (cmd == "0x05"):
                    rst = self.ble_specail.Special_BLE_Mode_prase(cmd, base64_data)
                if (cmd == "0x10"):
                    rst = self.ble_specail.Special_BLE_SensorData_prase(cmd, base64_data)
                if (cmd == "0x17"):
                    rst = self.ble_specail.Special_BLE_Abnormal_prase(cmd, base64_data)
                if (cmd == "0x19"):
                    rst = self.ble_specail.Special_BLE_State_prase(cmd, base64_data)
                if (cmd == "0x1F"):
                    rst = self.ble_specail.Special_BLE_Switch_prase(cmd, base64_data)
                if (cmd == "0x22"):
                    rst = self.ble_specail.Special_BLE_KeepWarm_prase(cmd, base64_data)
                if (cmd == "0x23"):
                    rst = self.ble_specail.Special_BLE_Reserve_prase(cmd, base64_data)
                if (cmd == "0x16"):
                    rst = self.ble_specail.Special_BLE_Display_prase(cmd, base64_data)
                if (cmd == "0x08"):
                    rst = self.ble_specail.Special_BLE_SlaveDevice_prase(cmd, base64_data)
                if (cmd == "0x1B"):
                    rst = self.ble_specail.Special_BLE_NightLight_prase(cmd, base64_data)
                self.utils.output_to_file(rst)

    def prase_py_info_output(self):
        localtime = time.asctime(time.localtime(time.time()))
        self.utils.output_to_file('SKU:' + str(SKU))
        self.utils.output_to_file('Version:' + str(Version))
        self.utils.output_to_file('DateAndTime:' + str(localtime))

    def prase_statistics_output(self):
        self.utils.output_to_file(' ------- statistics output -------')

    def prase_bizType_LWT_count(self, file_line):
        if -1 != file_line.find("LWT"):
            self.LWT_Count = self.LWT_Count + 1
            self.utils.output_to_file('LWT SKU:' + str(SKU))
            self.utils.output_to_file('')

    def prase_fromMSG_count(self, file_line):
        if -1 != file_line.find("from"):
            self.from_msg = self.utils.split_log(file_line, "from\":\"", "\",\"transaction")
            try:
                msg_index = From_Key_Tup.index(self.from_msg)
                self.Line_FromMSG = "from:" + str(self.from_msg) + " - " + str(From_KeyName_Tup[msg_index])
                self.From_KeyCount_List[msg_index] = self.From_KeyCount_List[msg_index] + 1
            except:
                self.From_KeyCount_List[-1] = self.From_KeyCount_List[-1] + 1
                self.Line_FromMSG = "from:" + str(self.from_msg) + str(From_KeyName_Tup[-1])

    def prase_LWT_output(self):
        self.utils.output_to_file('LWT:' + str(self.LWT_Count))

    def prase_fromMSG_output(self):
        msg_output_json = {}
        for x in range(len(self.From_KeyCount_List)):
            msg_output_json[From_KeyName_Tup[x]] = self.From_KeyCount_List[x]
        self.utils.output_to_file(
            'from:' + str(json.dumps(msg_output_json, sort_keys=True, indent=4, separators=(',', ':'))))

    def prase_json_info(self):
        try:
            self.log_dev_json = json.loads(str(self.log_json))
        except:
            return

        # print(self.log_dev_json)

        self.utils.output_to_file(self.Line_FromMSG)
        try:
            if 'warn' in self.log_dev_json:
                self.prase_general_info("warn:", self.log_dev_json['warn'])

            if 'type' in self.log_dev_json:
                self.prase_general_info("type:", self.log_dev_json['type'])

            if 'op' in self.log_dev_json:
                self.prase_BLE_decode(self.log_dev_json['op']['command'])

            if 'state' in self.log_dev_json:
                self.prase_status_info(self.log_dev_json['state'])

            if 'timestamp' in self.log_dev_json:
                self.prase_timestamp_info(self.log_dev_json['timestamp'])
        except Exception:
            pass
    def prase_data_line_split_handle(self, file_line):
        if -1 != file_line.find("bizType"):
            self.log_json = self.utils.split_log(file_line, "\"message\":\"", "\",\"@timestamp")
            new_string = self.utils.format_mac(file_line)
            new_string = self.utils.remove_log(new_string, "\"message\":\"", "\"@timestamp")
            self.utils.renew_log(new_string)
        else:
            self.log_json = ''

    def statistics_output(self):
        self.prase_statistics_output()
        self.prase_py_info_output()
        self.prase_LWT_output()
        self.prase_fromMSG_output()
        self.prase_statistics_output()

    def run_prase(self):
        Mqtt_Prase.prase_ble_protocol_init(self)
        file_all_lines = Mqtt_Prase.utils.in_file.readlines()
        for file_line in file_all_lines:
            Mqtt_Prase.prase_bizType_LWT_count(self, file_line)
            Mqtt_Prase.prase_fromMSG_count(self, file_line)
            Mqtt_Prase.prase_data_line_split_handle(self, file_line)
            Mqtt_Prase.prase_json_info(self)
        Mqtt_Prase.statistics_output(self)


# Init  --------------------------------------
def Log_Prase_Handle():
    C = Mqtt_Prase()
    C.run_prase()


if __name__ == '__main__':
    Log_Prase_Handle()
