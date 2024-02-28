import serial
import threading
import time
import datetime


class SerialAuto(object):

    def __init__(self, com, dbs, timeout):
        self.err = 0
        self.com = com
        self.dbs = dbs
        self.timeout = timeout
        self.err_date = ''  # 做是否有错误判断的数据
        self.txt_date = ''  # 写入TXT的数据
        self.err_count = 0  # 记录错误次数
        try:
            self.ser = serial.Serial(self.com,
                                     self.dbs,
                                     timeout=self.timeout)
            print("*********打开串口成功*********")
        except Exception as e:
            print("*********串口异常:{}*********".format(e))
            self.err = -1

    # 写入数据
    def write_date(self, write_itme):
        self.ser.write(write_itme.encode('UTF-8'))
        self.ser.write('\r'.encode())

    # 读取处理数据
    def read_date(self, check_date):
        check_edit = check_date
        check_dates = {}  # 断言数据
        while True:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S----->")
            is_success_date = ''  # 判断是否执行成功的临时数据
            # try:
            date_line = self.ser.readline().decode()
            time.sleep(0.1)
            is_success_date += date_line
            self.txt_date += str(date_line)  # 所有写入到txt文档
            # self.write_txt(self.txt_date)
            for i in range(len(check_edit)):
                # 开机:55 11 01 00 01 01 69, 关机:55 11 01 00 01 00 68
                check_dates[check_edit[i].split(":")[0]] = check_edit[i].split(":")[1]  # 将每个输入的键值对加入到字典里
                check_list = []
                for j in check_dates:
                    check_list.append(j)
                if check_dates[check_list[i]] in date_line:
                    success_date = str(now_time + check_list[i]) + "."
                    # print("{}成功".format(success_date))
                    self.err_date += success_date
                    self.txt_date += success_date
            # except Exception as e:
            #     print(e)

    # 判断错误数据
    def date_result(self, n):
        date = self.err_date.split('.')
        if len(date) - 1 == len(n):  # 因为split分隔后会多一段数据，所以-1
            for j in date:
                # print(j)
                pass  # 存入txt文档
            self.err_date = ''
        elif len(date) == 1:
            pass
        else:
            err_ = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S前的一次执行中有错误！！！"))
            self.txt_date += err_
            SerialAuto.write_txt(self.txt_date)
            print(err_)
            self.err_date = ''
            self.err_count += 1
        return self.err_count

    # 数据写入txt文档
    @staticmethod
    def write_txt(t):
        result = str(t)
        try:
            with open('log.txt', 'w') as file_handle:
                file_handle.write(result)
        except Exception as e:
            print("文件读写出错：", e)

    # 线程读取数据
    def thread_recv(self, d):
        try:
            thread = threading.Thread(target=self.read_date, args=(d,), daemon=True)
            thread.start()
        except Exception as e:
            print("无法启动线程:{}".format(e))


if __name__ == '__main__':
    program = SerialAuto('com9', 115200, 3)
    m = 0  # 统计测试次数
    check_dates = ["开机:55 10 01 00 01 01 68", "关机:55 10 01 00 01 00 67"
                   ]
    # 如果
    if program.err == 0:
        # print("初始化成功...")
        # test_count = int(input("输入需要测试的次数："))  # 测试的次数
        print("*********开启读取数据*********\r")
        program.thread_recv(check_dates)
        send_list = ['uart 0x01 0x00', 'uart 0x01 0x01',  # 开机
                     'uart 0xF0 0x00', 'uart 0xF0 0x01', 'uart 0xF0 0x03', 'uart 0xF0 0xfa', 'uart 0xF0 0xfc',
                     'uart 0xF0 0xff',  # 心跳
                     'uart 0xF1 0x00', 'uart 0xF1 0x01', 'uart 0xF1 0x03', 'uart 0xF1 0xfa', 'uart 0xF1 0xfc',
                     'uart 0xF0 0xff',  # 查询状态
                     'uart 0xF3 0x00', 'uart 0xF3 0x01', 'uart 0xF3 0x03', 'uart 0xF3 0xfa', 'uart 0xF3 0xfc',
                     'uart 0xF3 0xff',  # wifi状态灯
                     'uart 0x02 0x00', 'uart 0x02 0x01', 'uart 0x02 0x02', 'uart 0x02 0x03', 'uart 0x02 0x05',
                     'uart 0x02 0x04', 'uart 0x02 0xfb', 'uart 0x02 0xfc', 'uart 0x02 0xff',  # 模式档位
                     'uart 0x03 0x00 0x22', 'uart 0x03 0x01 0x12', 'uart 0x03 0x03 0x12', 'uart 0x03 0xfa 0x12',
                     'uart 0x03 0xfc 0x12','uart 0x03 0xff 0x12',  # 摆叶
                     'uart 0x04 0x0000', 'uart 0x04 0x4001', 'uart 0x04 0x45a0', "uart 0x04 0x45ff",  # 延时关闭
                     'uart 0x05 0x00', 'uart 0x05 0x01', 'uart 0x05 0x02', 'uart 0x05 0xfa', 'uart 0x05 0xfc',
                     'uart 0x05 0xff',  # 童锁
                     'uart 0x07 0x00', 'uart 0x07 0x01', 'uart 0x07 0x02', 'uart 0x07 0xfa', 'uart 0x07 0xfc',
                     'uart 0x07 0xff',  # 指示灯开关
                     'uart 0x08 0x32 ', 'uart 0x08 0xB2', 'uart 0x08 0x64', 'uart 0x08 0xE4', 'uart 0x08 0xfc',
                     'uart 0x08 0xff',  # 氛围灯开关
                     'uart 0x09 0x00', 'uart 0x09 0x01', 'uart 0x09 0x02', 'uart 0x09 0x03', 'uart 0x09 0x04',
                     'uart 0x09 0x05', 'uart 0x09 0xfa', 'uart 0x09 0xfc', 'uart 0x09 0xff',  # 恒温
                     'uart 0x15 0x0C 0x80', 'uart 0x15 0x0B 0xBB', 'uart 0x15 0x0A 0xBC', 'uart 0x15 0x1F 0x40',
                     'uart 0x15 0x0D 0xEF', 'uart 0x15 0x21 0x98',  # 设置目标温度

                     ]  # 关机
        while True:
            print("========第{}次测试开始========".format(m + 1))
            for i in range(len(send_list)):
                program.write_date(send_list[i])  # 写入数据
                time.sleep(1)
            print("========第{}次测试完成========".format(m + 1))
            # program.date_result(send_list)
            m += 1
            if m == 100000000000:
                print("所有测试完成,一共测试了{}次".format(m))
                print("*********出现了{}次错误*********".format(program.date_result(send_list)))
                break
