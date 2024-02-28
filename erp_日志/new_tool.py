import re
import datetime
import base64
import json
import time
import os

SKU = "H7145"
Version = "v1.0"

# 爬取原始日志的文件夹路径
file_path = r'C:\新数据'
# 输入用户的时区
USER_TIMEZONE = -4
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
    'ifttt',
    'diel rhythm',
    'siri',
    'poweron',
    'device',
    'linkage',
    'other',)
# from END -----------------------------------------------------


# BLE START -----------------------------------------------------
# 在 HEX 和 MEANING 按顺序填入对应的指令
# 后面版本延时指令从0x11改为0x26
BLE_Protocol_HEX = (
    '0x10',
    '0x26',
    '0x12',
    '0x13',
    '0x16',
    '0x1f'
)

BLE_Protocol_MEANING = (
    'sensor数据',
    '延时关机',
    '定时组',
    '定时器',
    '熄屏',
    '童锁'
)

BLE_Special_Protocol_HEX = (
    '0x05',
    '0x17',
    '0x1b',
    '0x1E',
    '0x22'

)

BLE_Special_Protocol_MEANING = (
    '模式',
    '异常状态',
    'RGB夜灯',
    '温湿度校准值',
    '水位续航'
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
    def __init__(self, log_file_in_name, out_file_name):
        try:
            self.in_file = open(log_file_in_name, mode='r', encoding='utf-8')
            self.out_file = open(out_file_name, mode='w', encoding='utf-8')
        except FileNotFoundError:
            print("create input file " + out_file_name)
            self.in_file = open(out_file_name, mode='w+', encoding='utf-8')

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
            new_str = self.insert_str(in_str, '', mac_addr.span()[0])
            new_str = self.insert_str(new_str, '', mac_addr.span()[1] + 1)
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
        print(range_red)
        print(range_green)
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
    def general_sensordata_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x80):
            info += "设备sensor离线"
        elif (data[2] == 0x81):
            info += "设备sensor在线"
        elif (data[2] == 0x00):
            info += "绑定温湿度计离线"
        elif (data[2] == 0x01):
            info += "绑定温湿度计在线"
        else:
            info += "异常"
        temp = (data[3] << 16) + (data[4] << 8) + data[5]
        humi = temp % 1000
        temper = (temp - humi) / 1000
        info += "当前湿度 {:f}".format(humi / 10)
        info += " 当前温度 {:f}".format(temper / 10)
        return str(BLE_Protocol[cmd]) + '-> ' + info

    def general_delayclose_count(self, cmd, data):
        info = ""
        if (data[2] == 0x01):
            info += "开启 "
        else:
            info += "关闭 "
        min_get = (data[3] << 8) + data[4]
        sec_get = (data[5] << 16) + (data[6] << 8) + data[7]
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
        if (data[3] & 0x02):
            info += "夜灯开"
        else:
            info += "夜灯关"
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
            low_grade = data[3] & 0x80
            if (low_grade == 0x80):
                info += "低档维持关闭 "
            else:
                info += "低档维持打开 "
            if (data[4] == 0x01):
                info += "舒适打开 "
            else:
                info += "舒适关闭 "
            tar_humi = data[3] & 0x7f
            info += "目标湿度 {:f}".format(tar_humi)
        elif (data[2] == 0x01):
            info += "挡位模式 "
            if (data[3] >= 0x01 and data[3] <= 0x09):
                info += "设置档位{:f}".format(data[3])
            else:
                info += "挡位参数错误"
        elif (data[2] == 0x08):
            info += "干衣模式 "
        elif (data[2] == 0x00):
            info += "当前模式为 "
            if (data[3] == 0x08):
                info += "干衣模式"
            elif (data[3] == 0x03):
                info += "自动模式"
            elif (data[3] == 0x01):
                info += "挡位模式 "
                # if (data[4] == 0x01):
                #     info += "低挡"
                # elif (data[4] == 0x03):
                #     info += "高挡"
                # else:
                #     info += "挡位参数错误"
        else:
            info += "模式参数错误"
        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_abnormal_prase(self, cmd, data):
        info = ""
        if ((data[2] == 0x00) and (data[3] == 0x00) and (data[4] == 0x00) and (data[5] == 0x00)):
            info += "无异常 "
        else:
            if (data[2] == 0x01):
                info += "72小时清洗提醒 "
            if (data[3] == 0x01):
                info += "缺水 "
            elif (data[3] == 0x04):
                info += "干烧"
            elif (data[3] == 0x20):
                info += "水箱提起"
            elif (data[3] == 0x40):
                info += "高水位"
            else:
                info += "无异常"
            if (data[4] == 0x01):
                info += "自动模式下待机 "
            elif (data[4] == 0x02):
                info += "自动模式下低档维持"
            else:
                info += ""
        # info += "超声波检测原始数据{"
        # for i in 6:
        #     info += "数据{:f}".format([data[i+6]])
        info += "超声波检测高度数据{:f}".format(data[13])
        info += "  "
        info += "回波时长{:f}".format(data[14])

        return str(BLE_Special_Protocol[cmd]) + '-> ' + info

    def Special_HumiTemp_Cali_prase(self, cmd, data):
        info = ""
        cali_data = data[4] << 8 or data[5]
        if (data[2] == 0x01):
            info += "温度校准："
            if (data[3] == 0x01):
                info += "绑定sensor{:f}".format(cali_data)
            else:
                info += "设备sensor{:f}".format(cali_data)
        elif (data[2] == 0x02):
            info += "湿度校准："
            if (data[3] == 0x01):
                info += "绑定sensor{:f}".format(cali_data)
            else:
                info += "设备sensor{:f}".format(cali_data)
        return str(BLE_Special_Protocol[cmd] + '->' + info)

    def Special_RGB_prase(self, cmd, data):
        info = ""
        if (data[2] == 0x01):
            if (data[3] == 0x01):
                info += "夜灯开"
                info += "亮度：{:f}".format(data[4])
            else:
                info += "夜灯关"
        elif (data[2] == 0x05):
            if (data[3] == 0x0D):
                info += "颜色模式"
            elif (data[3] == 0x13):
                if (data[5] == 0x01):
                    info += "场景模式:森林"
                elif (data[5] == 0x02):
                    info += "场景模式:海洋"
                elif (data[5] == 0x03):
                    info += "场景模式:湿地"
                elif (data[5] == 0x04):
                    info += "场景模式：悠闲"
                elif (data[5] == 0x05):
                    info += "场景模式：安眠"
                else:
                    info += ""
            elif (data[3] == 0x0a):
                info += "DIY模式"
            else:
                info += ""
        return str(BLE_Special_Protocol[cmd] + '->' + info)

    def Special_Water_Battery_prase(self, cmd, data):
        info = ""
        battery = data[3] << 8 or data[4]
        info += "水位{:f}".format(data[2])
        info += "续航时间{:f}".format(battery)
        return str(BLE_Special_Protocol[cmd] + '->' + info)

    def Special_BLE_xxx_prase(self, data):
        return "Special_BLE_xxx_prase"

def Analyze(utils_s_s):
    # class Mqtt_Prase START --------------------------------------
    class Mqtt_Prase:
        utils = utils_s_s
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
            stc = "op: " + str(i_info[0:2])
            if (i_info[3] == '0'):
                stc = stc + " ,boot : 断电上电"
            elif (i_info[3] == '1'):
                stc = stc + " ,boot : 主动重启"
            else:
                stc = stc + " ,boot : 异常，需注意！！！！！"
            stc = stc + " , RSSI: " + str(i_info[5:7])
            stc = stc + " , Running: " + str(i_info[8:])
            self.utils.output_to_file("stc: " + stc)

        def prase_status_info(self, i_info):
            if "onOff" in i_info:
                self.utils.output_to_file("onoff:" + str(i_info["onOff"]))
            if "sta" in i_info:
                self.utils.output_to_file("sta:" + str(i_info["sta"]))
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
                    if (cmd == "0x10"):
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
                        rst = self.ble_specail.Special_abnormal_prase(cmd, base64_data)
                    elif (cmd == "0x1E"):
                        rst = self.ble_specail.Special_HumiTemp_Cali_prase(cmd, base64_data)
                    elif (cmd == "0x1b"):
                        rst = self.ble_specail.Special_RGB_prase(cmd, base64_data)
                    elif (cmd == "0x22"):
                        rst = self.ble_specail.Special_Water_Battery_prase(cmd, base64_data)
                    self.utils.output_to_file(rst)

        def prase_py_info_output(self):
            localtime = time.asctime(time.localtime(time.time()))
            self.utils.output_to_file('SKU:' + str(SKU))
            self.utils.output_to_file('Version:' + str(Version))
            self.utils.output_to_file('DateAndTime:' + str(localtime))
            # if 'device' in self.log_dev_json:
                # self.parce_py_device_id((self.log_dev_json['device']))
            # id = self.log_dev_json['device']
            # print('~~~~~~~:'+str(id))
        def prase_statistics_output(self):
            self.utils.output_to_file(' ------- statistics output -------')

        def prase_bizType_LWT_count(self, file_line):
            if -1 != file_line.find("LWT"):
                self.LWT_Count = self.LWT_Count + 1
                self.utils.output_to_file('SKU:' + str(SKU))

        def prase_fromMSG_count(self, file_line):
            if -1 != file_line.find("from"):
                self.from_msg = self.utils.split_log(file_line, "from\':\'", "\',\'transaction")
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
            # if -1 != file_line.find("bizType"):
            #     self.log_json = self.utils.split_log(file_line, "\"message\":\"", "\",\"@timestamp")
            #     new_string = self.utils.format_mac(file_line)
            #     new_string = self.utils.remove_log(new_string, "\"message\":\"", "\"@timestamp")
            #     self.utils.renew_log(new_string)
            if -1 != file_line.find("bizType"):
                file_line.find("")
                file_line = file_line.replace("\'","\"")

                # print("//////////////////////")
                self.log_json = self.utils.split_log(file_line, "\"message\":", ", \"@timestamp\"")
                new_string = self.utils.format_mac(file_line)
                # print(new_string)
                new_string = self.utils.remove_log(new_string, "message", "@timestamp")
                # print("+++++++++")
                # print(new_string)
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
            print("========================================")
            print('解析中..........')
            print("========================================")
            Mqtt_Prase.prase_ble_protocol_init(self)
            file_all_lines = Mqtt_Prase.utils.in_file.readlines()
            for file_line in file_all_lines:
                Mqtt_Prase.prase_bizType_LWT_count(self,  file_line)
                Mqtt_Prase.prase_fromMSG_count(self, file_line)
                Mqtt_Prase.prase_data_line_split_handle(self, file_line)
                Mqtt_Prase.prase_json_info(self)
            Mqtt_Prase.statistics_output(self)
    C = Mqtt_Prase()
    C.run_prase()

# Init  --------------------------------------
def Log_Prase_Handle():
    file_list = os.listdir(file_path)
    for file_name in file_list:
        print('读取' + file_name)
        file = os.path.join(file_path, file_name)
        out_file_name = file_name.split('.')[0] +'_'+ '解析日志.txt'
        utils = Mqtt_Utils(file, out_file_name)
        Analyze(utils)
        print("========================================")
        print(file_name + '解析完成')
        print("========================================")


if __name__ == '__main__':
    Log_Prase_Handle()
