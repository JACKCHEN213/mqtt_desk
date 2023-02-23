# -*- coding: utf-8 -*-
"""
MQTT服务
"""
from model.mqtt import MqttConfig
from utils.log import Log
from config import LOG_CONFIG
from typing import Dict, Union
from collections import defaultdict
import json
import time
from paho.mqtt import client as mqtt_client
from paho.mqtt.client import connack_string, MQTTMessage
from queue import Queue



class MQTT:
    client_instance = None
    mqtt_queue = Queue()

    def __init__(self, mqtt_config: Union[Dict, MqttConfig, None] = None):
        """
        阻塞获取mqtt服务
        :param mqtt_config: mqtt服务配置
        """
        self.logger = Log('mqtt', LOG_CONFIG)

        if mqtt_config is None:
            mqtt_config = MqttConfig()
        elif isinstance(mqtt_config, dict):
            mqtt_config = MqttConfig(**mqtt_config)
        self.mqtt_config = mqtt_config

        self.client = mqtt_client.Client(mqtt_config.client_id, reconnect_on_failure=False)
        self.client.on_connect = self.__connected
        self.__connection()

        self.client_instance = self
        self.client.loop_start()
        self.__test_is_connect()

        self.subscribes = defaultdict(list)

        # NOTE: 阻塞获取连接结果
        if isinstance(msg := self.mqtt_queue.get(), str):
            raise Exception(msg)

    def __test_is_connect(self):
        """
        测试mqtt是否完成连接
        :return:
        """
        self.publish('/mqtt/test', 'connected')
        self.mqtt_config.connection_time = int(time.time())

    def __connection(self):
        """
        重新连接客户端
        :return:
        """
        self.client.username_pw_set(self.mqtt_config.username, self.mqtt_config.password)
        self.client.connect(self.mqtt_config.ip, self.mqtt_config.port)

    def __connected(self, _, __, ___, rc):
        if rc == 0:
            self.logger.info(f'mqtt连接成功，{self.mqtt_config.__str__()}')
            self.mqtt_queue.put(True)
        else:
            self.logger.warning(f'mqtt连接失败，错误原因：{connack_string(rc)}')
            self.mqtt_queue.put(connack_string(rc))

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

    def disconnect(self):
        """
        断开连接
        """
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info(f'断开mqtt连接，{self.mqtt_config.__str__()}')

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
                repr(e)
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
