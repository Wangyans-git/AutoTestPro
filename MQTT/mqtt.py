import datetime
import ssl
import json
import paho.mqtt.client as mqtt


class MQTTClient:
    mqtt_data = None

    def mqttclient(self, mqtt_topic, formal_or_test):
        if formal_or_test:
            mqtt_broker = "aqm3wd1qlc3dy.iot.us-east-1.amazonaws.com"
            mqtt_port = 8883
            mqtt_client_id = "mqttx_b12cd818"
            mqtt_client = mqtt.Client(client_id=mqtt_client_id)  # 创建MQTT客户端
            mqtt_client.on_message = self.mqtt_message
            mqtt_client.tls_set(ca_certs=f"Conf/root-CA.crt",
                                certfile="Conf/testIot.cert.pem",
                                keyfile="Conf/testIot.private.key",
                                cert_reqs=ssl.CERT_REQUIRED,
                                tls_version=ssl.PROTOCOL_TLSv1_2)
        else:
            mqtt_broker = "a3d1vz6v56pkuw-ats.iot.us-east-1.amazonaws.com"
            mqtt_port = 8883
            mqtt_client_id = "mqttx_2bd59eaf"
            mqtt_client = mqtt.Client(client_id=mqtt_client_id)  # 创建MQTT客户端
            mqtt_client.on_message = self.mqtt_message
            mqtt_client.tls_set(ca_certs=f"dev_Conf/rootCA.pem",
                                certfile="dev_Conf/b2f000de59-certificate.pem.crt",
                                keyfile="dev_Conf/b2f000de59-private.pem.key",
                                cert_reqs=ssl.CERT_REQUIRED,
                                tls_version=ssl.PROTOCOL_TLSv1_2)
        mqtt_client.connect(mqtt_broker, mqtt_port)
        mqtt_client.subscribe(mqtt_topic)
        # 开启MQTT循环监听
        mqtt_client.loop_forever()
        return mqtt_client

    def mqtt_stop(self, mqtt_client):
        mqtt_client.loop_stop()
        # 断开MQTT连接
        mqtt_client.disconnect()

    def mqtt_message(self, client, userdata, msg):
        # 处理收到的MQTT消息
        if msg.payload.decode('UTF-8'):
            dist_date = json.loads(msg.payload.decode('UTF-8'))
            now_time = datetime.datetime.now()
            formatted_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
            print("{0}\n{1}\n".format(formatted_time,dist_date))
            mqtt_data = msg.payload.decode('UTF-8')
            return mqtt_data
        else:
            print("该灯效没有MQTT消息下发")


if __name__ == '__main__':
    formal_or_test = 0 # 1正服  0测服
    # 正服
    # r = MQTTClient().mqttclient("GA/760c770c58dffc6523c87e135f0a65d8", formal_or_test)
    # 测服
    # r = MQTTClient().mqttclient("GA/305159cf7e83a942becdb879f59b6d76", formal_or_test)
    r = MQTTClient().mqttclient("GD/fc0b1f2ba94a615ef52542aff180556b", formal_or_test)
