# coding=UTF-8

import time
import socket
import json

# 组播组IP和端口
mcast_group_ip = '192.168.50.117'
# mcast_group_ip = '192.168.50.221'
mcast_group_port = 4003
# mcast_group_ip = '239.255.255.250'
# mcast_group_port = 4001




def sender():
    count = 0
    # 建立发送socket，和正常UDP数据包没区别
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # 1.IPV4  2.UDP
    local_addr = ('', 4002)
    send_sock.bind(local_addr)
    # 每十秒发送一遍消息
    while count<1:


        # cmd_json = {
        #     "msg": {
        #         "cmd": "turn",
        #         "data": {
        #             "value": 0
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("turn off\r\n")
        # time.sleep(1)

        # 查询状态
        # cmd_json = {
        #     "msg": {
        #         "cmd": "devStatus",
        #         "data": {
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("get devStatus\r\n")
        # recv_data = send_sock.recvfrom(1024)
        #
        # recv_msg = recv_data[0]
        # send_addr = recv_data[1]
        # print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        # time.sleep(1)
        #

        # cmd_json = {
        #     "msg": {
        #         "cmd": "turn",
        #         "data": {
        #             "value": 1
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("turn on\r\n")
        # time.sleep(2)
        # #
        # # 查询状态
        # cmd_json = {
        #     "msg": {
        #         "cmd": "devStatus",
        #         "data": {
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("get devStatus\r\n")
        # recv_data = send_sock.recvfrom(1024)
        #
        # recv_msg = recv_data[0]
        # send_addr = recv_data[1]
        # print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        # time.sleep(1)
        #
        # cmd_json = {
        #     "msg": {
        #         "cmd": "brightness",
        #         "data": {
        #             "value": ''
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("set brightness 1\r\n")
        # time.sleep(2)
        #
        # # 查询状态
        # cmd_json = {
        #     "msg": {
        #         "cmd": "devStatus",
        #         "data": {
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("get devStatus\r\n")
        # recv_data = send_sock.recvfrom(1024)
        # #
        # recv_msg = recv_data[0]
        # send_addr = recv_data[1]
        # print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        # time.sleep(1)
        #
        # cmd_json = {
        #     "msg": {
        #         "cmd": "brightness",
        #         "data": {
        #             "value": 100
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("set brightness 100\r\n")
        # time.sleep(2)
        #
        # # 查询状态
        # cmd_json = {
        #     "msg": {
        #         "cmd": "devStatus",
        #         "data": {
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("get devStatus\r\n")
        # recv_data = send_sock.recvfrom(1024)
        #
        # recv_msg = recv_data[0]
        # send_addr = recv_data[1]
        # print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        # time.sleep(1)
        #
        # cmd_json = {
        #     "msg": {
        #         "cmd": "colorwc",
        #         "data": {
        #             "color": {
        #                 "r": 0,
        #                 "g": 255,
        #                 "b": 0
        #             }
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("set red\r\n")
        # time.sleep(2)
        #
        # # 查询状态
        # cmd_json = {
        #     "msg": {
        #         "cmd": "devStatus",
        #         "data": {
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("get devStatus\r\n")
        # recv_data = send_sock.recvfrom(1024)
        #
        # recv_msg = recv_data[0]
        # send_addr = recv_data[1]
        # print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        # time.sleep(1)
        #
        # cmd_json = {
        #     "msg": {
        #         "cmd": "colorwc",
        #         "data": {
        #             "color": {
        #                 "r": 0,
        #                 "g": 255,
        #                 "b": 0
        #             }
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("set green\r\n")
        # time.sleep(2)
        # #
        # # 查询状态
        # cmd_json = {
        #     "msg": {
        #         "cmd": "devStatus",
        #         "data": {
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("get devStatus\r\n")
        # recv_data = send_sock.recvfrom(1024)
        #
        # recv_msg = recv_data[0]
        # send_addr = recv_data[1]
        # print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        # time.sleep(1)
        #
        # cmd_json = {
        #     "msg": {
        #         "cmd": "colorwc",
        #         "data": {
        #             "color": {
        #                 "r": 0,
        #                 "g": 0,
        #                 "b": 255
        #             }
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("set blue\r\n")
        # time.sleep(2)
        # #
        # # 查询状态
        # cmd_json = {
        #     "msg": {
        #         "cmd": "devStatus",
        #         "data": {
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("get devStatus\r\n")
        # recv_data = send_sock.recvfrom(1024)
        #
        # recv_msg = recv_data[0]
        # send_addr = recv_data[1]
        # print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        # time.sleep(1)
        #
        # 色温
        # cmd_json = {
        #     "msg": {
        #         "cmd": "colorwc",
        #         "data": {
        #             "color": {"r": 0, "g": 255, "b": 255},
        #             "colorTemInKelvin": None
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("set cw 2000\r\n")
        # time.sleep(5)

        # 查询状态
        cmd_json = {
            "msg": {
                "cmd": "devStatus",
                "data": {
                }
            }
        }
        message = json.dumps(cmd_json)
        # 发送写法和正常UDP数据包的还是完全没区别
        # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        print("get devStatus\r\n")
        recv_data = send_sock.recvfrom(1024)

        recv_msg = recv_data[0]
        send_addr = recv_data[1]
        print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        time.sleep(1)
        # #
        # cmd_json = {
        #     "msg": {
        #         "cmd": "colorwc",
        #         "data": {
        #             "color": {"r": 255, "g": 0, "b": 0},
        #             "colorTemInKelvin": 6500
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("set cw 9000\r\n")
        # time.sleep(5)
        # #
        # # 查询状态
        # cmd_json = {
        #     "msg": {
        #         "cmd": "devStatus",
        #         "data": {
        #         }
        #     }
        # }
        # message = json.dumps(cmd_json)
        # # 发送写法和正常UDP数据包的还是完全没区别
        # # 猜测只可能是网卡自己在识别到目的ip是组播地址后，自动将目的mac地址设为多播mac地址
        # send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        # print("get devStatus\r\n")
        # recv_data = send_sock.recvfrom(1024)
        #
        # recv_msg = recv_data[0]
        # send_addr = recv_data[1]
        # print("%s:%s\r\n" % (str(send_addr), recv_msg.decode("gbk")))
        # time.sleep(1)
        count += 1
        print("第{}次测试完成".format(count))


if __name__ == "__main__":
    sender()
