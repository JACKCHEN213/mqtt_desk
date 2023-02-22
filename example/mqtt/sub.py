# -*- coding: utf-8 -*-
import os
import sys
os.chdir(os.path.abspath(os.path.dirname(__file__) + '/../..'))
sys.path.append('.')
from common.mqtt import MQTT
from model.mqtt import MqttConfig
from config.configuration import Configuration
from config import CONFIG_DIR


def print_topic(data, topic):
    print(data)
    print(topic)


if __name__ == '__main__':
    mqtt_client = MQTT.get_instance(
        MqttConfig(**Configuration.load_config(CONFIG_DIR + 'default.ini').get('mqtt', dict()))
    )
    mqtt_client.subscribe('/test', print_topic)
    mqtt_client.run()
