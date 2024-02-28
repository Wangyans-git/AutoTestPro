import re
import datetime
import base64
import json
import time

import chardet

SKU = "H7131"
Version = "v1.0"

LOG_FILE_NAME = "in_log.txt"
DECODE_FILE_NAME = "out_log.txt"
# 输入用户的时区
USER_TIMEZONE = -8
# This website could query the location of timezone all around the world
# https://www.zeitverschiebung.net/cn/
# New York City -5
# Los Angeles   -8

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
#后面版本延时指令从0x11改为0x26
BLE_Protocol_HEX = (
    '0x08',
    '0x10',
    '0x26',
    '0x12',
    '0x13',
    '0x16',
    '0x1f',
)

BLE_Protocol_MEANING = (
    'sensor地址',
    'sensor数据',
    '延时关机',
    '定时组',
    '定时器',
    '显示',
    '开关类操作',
)

BLE_Special_Protocol_HEX = (
    '0x05',
    '0x17',
    '0x19',
    '0x1a',
    '0x1b',
    '0x1e',
    '0x23',
)

BLE_Special_Protocol_MEANING = (
    '模式',
    '异常状态',
    '24H保护剩余时间',
    '恒温功能',
    'RGB灯',
    '校准值',
    '节能统计',
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
    def general_sensoraddr_prase(self, cmd, data):
        info = ""
        if ((data[2] == 0x00) and (data[3] == 0x00) 
        and (data[4] == 0x00) and (data[5] == 0x00) 
        and (data[6] == 0x00) and (data[7] == 0x00)):
            info += "未绑定 "
        else:
            info += "已绑定sensor " + '{:>02x}'.format(data[7]) + ':' + '{:>02x}'.format(data[6]) \
            + ':' + '{:>02x}'.format(data[5]) + ':' + '{:>02x}'.format(data[4]) \
            + ':' + '{:>02x}'.format(data[3]) + ':' + '{:>02x}'.format(data[2])
        return str(BLE_Protocol[cmd]) + '-> ' + info

    def general_sensordata_prase(self, cmd, data):
        info = ""
        if ((data[2]&0x01) == 0x01):
            info += "sensor在线 "
        else:
            info += "sensor离线 "
        if (data[2]>>7 == 0x01):
            info += "自带sensor "
        else:
            info += "联动sensor "
        temp = ((data[3]&0x7F) << 16) + (data[4] << 8) + data[5]
        humi = temp % 1000
        temper = (temp - humi) / 1000
        if (data[3]>>7):
            temper = -temper
        info += "当前湿度{:.2f} ".format(humi/10)
        if (data[6] == 0x01):
            info += " 当前温度华氏{:.2f}转摄氏{:.2f}".format(temper/10, (temper/10-32)*5/9)
        else:
            info += " 当前温度摄氏{:.2f}".format(temper/10)
        return str(BLE_Protocol[cmd]) + '-> ' + info

    def general_delayclose_count(self, cmd, data):
        info = ""
        if (data[2] == 0x01):
            info += "开启 "
        else:
            info += "关闭 "
        min_get = (data[3]<<8) + data[4]
        sec_get = (data[5]<<16) + (data[6]<<8) + data[7]
        info += "设置分钟数 {:d}".format(min_get)
        info += " 剩余秒数 {:d}".format(sec_get)
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

    def general_display_prase(self, cmd, data):
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
        return str(BLE_Protocol[cmd]) + '-> ' + info

    def general_operate_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x01):
            info += "摇头开启 "
        else:
            info += "摇头关闭 "
        if (data[3] == 0x01):
            info += "童锁开启 "
        else:
            info += "童锁关闭 "
        return str(BLE_Protocol[cmd]) + '-> ' + info

# class Special_BLE START --------------------------------------
# SKU 特有协议解析
class Special_BLE:
    def Special_BLE_Mode_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x03):
            info += "自动模式 "
            if (data[3] == 0x01):
                info += "自动停止打开 "
            else:
                info += "自动停止关闭 "
            target_type = data[4]>>7
            target_temp = ((data[4]& 0x7F) << 8) + data[5]
            if (target_type == 0x01):
                info += "目标华氏{:.2f}转摄氏为{:.2f} ".format(target_temp/100, (target_temp/100-32)*5/9)
            else:
                info += "目标摄氏{:.2f} ".format(target_temp/100)
        elif (data[2] == 0x01):
            info += "挡位模式 "
            if (data[3] == 0x01):
                info += "低挡"
            elif (data[3] == 0x02):
                info += "中挡"
            elif (data[3] == 0x03):
                info += "高挡"
            else:
                info += "挡位参数错误"
        elif (data[2] == 0x09):
            info += "风扇模式 "
        elif (data[2] == 0x00):
            info += "当前模式为 "
            if (data[3] == 0x01):
                info += "挡位模式"
            elif (data[3] == 0x03):
                info += "自动模式"
            elif (data[3] == 0x09):
                info += "风扇模式 "
        else:
            info += "模式参数错误"
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_Abnormal_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x00):
            info += "无锁定 "
        elif (data[2] == 0x01):
            info += "锁定中 "
        else:
            info += "参数错误 "
        if (data[3] == 0x01):
            info += "上电保护"
        elif (data[3] == 0x02):
            info += "过热保护"
        elif (data[3] == 0x03):
            info += "24H保护"
        elif (data[3] == 0x04):
            info += "倾倒保护"
        elif (data[3] == 0x05):
            info += "NTC失效"
        if (data[4] == 0x01):
            info += "过热保护"
        if (data[5] == 0x01):
            info += "24H保护"
        if (data[6] == 0x01):
            info += "倾倒保护"
        if (data[7] == 0x01):
            info += "NTC失效"
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_24HRemainTime_prase(self, cmd, data):
        info = ""
        get_24h_min = (data[2]<<8) + data[3]
        info += "{:d} ".format(get_24h_min)
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_Thermostat_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x00):
            info += "关闭 "
        elif (data[2] == 0x01):
            info += "开启 "
        else:
            info += "参数错误 "
        if (data[3] == 0x00):
            info += "自动停止关闭 "
        elif (data[3] == 0x01):
            info += "自动停止开启 "
        else:
            info += "参数错误 "
        target_type = data[4]>>7
        target_temp = ((data[4]& 0x7F) << 8) + data[5]
        if (target_type == 0x01):
            info += "目标华氏{:.2f}转摄氏为{:.2f} ".format(target_temp/100, (target_temp/100-32)*5/9)
        else:
            info += "目标摄氏{:.2f} ".format(target_temp/100)
        
        highTarget = (data[6] << 8) + data[7]
        lowTarget = (data[8] << 8) + data[9]
        info += "范围{:d}-{:d} ".format(lowTarget, highTarget)

        offset_tham = 10
        if (data[offset_tham] & 0x01):
            info += "在线 "
        else:
            info += "离线 "
        if ((data[offset_tham] & 0x80)>>7):
            info += "NTC"
        else:
            info += "温度计"
        temp = ((data[offset_tham + 1]&0x7F) << 16) + (data[offset_tham + 2] << 8) + data[offset_tham + 3]
        humi = temp % 1000
        temper = (temp - humi) / 1000
        if (data[offset_tham + 1]>>7):
            temper = -temper
        info += "湿度{:.2f} ".format(humi/10)    
        if (data[offset_tham + 4] == 0x01):
            info += "华氏{:.2f}转摄氏{:.2f} ".format(temper/10, (temper/10-32)*5/9)
        else:
            info += "摄氏{:.2f} ".format(temper/10)
        info += "偏移时间{:d} ".format(data[10])
        if (data[offset_tham + 5] == 0x01):
            info += "恒温下待机 "
        elif (data[offset_tham + 5] == 0x00):
            info += "非恒温下待机 "
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_RGB_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x01):
            if (data[3] == 0x00):
                info += "RGB关闭 "
            elif (data[3] == 0x01):
                info += "RGB打开 "
            info += "亮度{:d}".format(data[4])
        elif (data[2] == 0x05):
            if (data[3] == 0x0a):
                info += "DIY模式 "
                code_value = (data[4]<<8) + data[5]
                info += "Code值{:d}".format(code_value)
            elif (data[3] == 0x0d):
                info += "颜色模式 "
                info += "R:{:d} ".format(data[4])
                info += "G:{:d} ".format(data[5])
                info += "B:{:d} ".format(data[6])
            elif (data[3] == 0x13):
                info += "场景模式 "
                if (data[5] == 0x01):
                    info += "火焰 "
                elif (data[5] == 0x02):
                    info += "彩虹 "
                elif (data[5] == 0x03):
                    info += "律动 "
                elif (data[5] == 0x04):
                    info += "悠闲 "
                elif (data[5] == 0x05):
                    info += "安眠 "
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info


    def Special_BLE_Calivalue_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x01):
            info += "温度 "
            if (data[3] == 0x01):
                info += "温度计校准 "
            elif (data[3] == 0x02):
                info += "NTC校准 "
            else:
                info += "解析异常 "
            cail_value = ((data[4] & 0x7f) << 8) + data[5]
            signs = data[4]>>7
            if (signs == 0x01):
                cail_value = -cail_value
            info += "校准值为{:.2f}".format(cail_value / 100)
        else:
            info += "类型异常 "
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_BLE_Energy_prase(self, cmd, data):
        info = ""
        run_time = (data[2] << 24) + (data[3] << 16) + (data[4] << 8) + data[5]
        info += "运行时间:{:.1f}小时 ".format(run_time / 10)
        save_energy = (data[6] << 24) + (data[7] << 16) + (data[8] << 8) + data[9]
        info += "节能:{:.1f}Kwh".format(save_energy / 10)
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
            'User:' + str(datetime.datetime.fromtimestamp((timestamp / 1000) + (USER_TIMEZONE - 8) * 3600)))
        self.utils.output_to_file('----------------------------\r')

    def prase_BLE_decode(self, info):
        for i in info:
            base64_data = base64.b64decode(i)
            self.prase_general_info("", self.utils.format_hex(base64_data))
            cmd = '0x{:>02x}'.format(base64_data[1])
            if (cmd in BLE_Protocol):
                if (cmd == "0x08"):
                    rst = self.ble_decode.general_sensoraddr_prase(cmd, base64_data)
                elif (cmd == "0x10"):
                    rst = self.ble_decode.general_sensordata_prase(cmd, base64_data)
                elif (cmd == "0x26"):
                    rst = self.ble_decode.general_delayclose_count(cmd, base64_data)
                elif (cmd == "0x12"):
                    rst = self.ble_decode.general_timer_count(cmd, base64_data[2])
                elif (cmd == "0x13"):
                    rst = self.ble_decode.general_timer_prase(cmd, base64_data)
                elif (cmd == "0x16"):
                    rst = self.ble_decode.general_display_prase(cmd, base64_data)
                elif (cmd == "0x1f"):
                    rst = self.ble_decode.general_operate_prase(cmd, base64_data)
                self.utils.output_to_file(rst)

            if (cmd in BLE_Special_Protocol):
                if (cmd == "0x05"):
                    rst = self.ble_specail.Special_BLE_Mode_prase(cmd, base64_data)
                elif (cmd == "0x17"):
                    rst = self.ble_specail.Special_BLE_Abnormal_prase(cmd, base64_data)
                elif (cmd == "0x19"):
                    rst = self.ble_specail.Special_BLE_24HRemainTime_prase(cmd, base64_data)
                elif (cmd == "0x1a"):
                    rst = self.ble_specail.Special_BLE_Thermostat_prase(cmd, base64_data)
                elif (cmd == "0x1b"):
                    rst = self.ble_specail.Special_BLE_RGB_prase(cmd, base64_data)
                elif (cmd == "0x1e"):
                    rst = self.ble_specail.Special_BLE_Calivalue_prase(cmd, base64_data)
                elif (cmd == "0x23"):
                    rst = self.ble_specail.Special_BLE_Energy_prase(cmd,base64_data)
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
        if self.log_dev_json == -1:
            return

        self.utils.output_to_file(self.Line_FromMSG)
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
