# -*- coding: utf-8 -*-
"""
MQTT服务
"""
from model.mqtt import MqttConfig
from typing import Dict, Union
from collections import defaultdict
import json
import time
from paho.mqtt import client as mqtt_client
from paho.mqtt.client import connack_string, MQTTMessage


class MQTT:
    client_instance = None

    def __init__(self, mqtt_config: Union[Dict, MqttConfig, None] = None):
        """
        阻塞获取mqtt服务
        :param mqtt_config: mqtt服务配置
        """
        if mqtt_config is None:
            mqtt_config = MqttConfig()
        elif isinstance(mqtt_config, dict):
            mqtt_config = MqttConfig(**mqtt_config)
        self.mqtt_config = mqtt_config

        self.__client = mqtt_client.Client(mqtt_config.client_id)
        self.__client.on_connect = self.__connected
        self.__reconnection()

        self.client_instance = self
        self.__client.loop_start()
        self.__test_is_connect()

        self.subscribes = defaultdict(list)

    def __test_is_connect(self):
        """
        测试mqtt是否完成连接
        :return:
        """
        self.publish('/mqtt/test', 'connected')
        self.mqtt_config.connection_time = int(time.time())

    @property
    def client(self):
        while not self.mqtt_config.is_connected:
            """
            判断mqtt是否连接成功
            """
            if self.mqtt_config.max_retries <= self.mqtt_config.retries:
                raise Exception('MQTT连接失败')
            time.sleep(0.5)
        return self.__client

    def __reconnection(self):
        """
        重新连接客户端
        :return:
        """
        print(f'第{self.mqtt_config.retries + 1}次连接MQTT')
        self.mqtt_config.retries += 1
        self.mqtt_config.current_retries += 1

        self.__client.username_pw_set(self.mqtt_config.username, self.mqtt_config.password)
        self.__client.connect(self.mqtt_config.ip, self.mqtt_config.port)

    def __connected(self, _, __, ___, rc):
        if rc == 0:
            print('mqtt连接成功')
            self.mqtt_config.is_connected = True
            self.mqtt_config.retries = 0
        else:
            print('mqtt连接失败，错误原因：', connack_string(rc))
            time.sleep(self.mqtt_config.retries_interval)
            if self.mqtt_config.retries >= self.mqtt_config.max_retries:
                raise Exception('尝试连接超过最大连接数，mqtt连接失败')
            else:
                self.__reconnection()

    @classmethod
    def get_instance(cls, config=None):
        if config is None:
            config = dict()
        if cls.client_instance is None:
            cls.client_instance = cls(config)
        return cls.client_instance

    def run(self):
        """
        阻塞运行
        :return:
        """
        self.client.loop_forever()

    def publish(self, topic: str, data):
        """
        发布topic
        :param topic:
        :param data:
        :return:
        """
        if not isinstance(data, str):
            data = json.dumps(data)
        self.client.publish(topic, data)

    def subscribe(self, topic, callback):
        """
        监听topic
        :param topic:
        :param callback:
        :return:
        """

        def on_message(_, __, msg: MQTTMessage):
            try:
                data = eval(msg.payload.decode('utf-8'))
            except Exception as e:
                print(e)
                data = msg.payload.decode('utf-8')
            callback(data, msg.topic)

        if callback not in self.subscribes[topic]:
            self.subscribes[topic].append(callback)
        self.client.subscribe(topic)
        self.client.on_message = on_message

    def unsubscribe(self, topic):
        """
        取消topic的监听
        :param topic:
        :return:
        """
        if self.subscribes[topic]:
            self.client.unsubscribe(topic)
            del self.subscribes[topic]


__all__ = ['MQTT']
