# -*- coding: utf-8 -*-
import os
import sys
os.chdir(os.path.abspath(os.path.dirname(__file__) + '/../..'))
sys.path.append('.')
from common.mqtt import MQTT
from config.configuration import Configuration
from config import CONFIG_DIR
from model.mqtt import MqttConfig
import time


if __name__ == '__main__':
    mqtt_client = MQTT.get_instance(
        MqttConfig(**Configuration.load_config(CONFIG_DIR + 'default.ini').get('mqtt', dict()))
    )
    while True:
        mqtt_client.publish('/test', 'hello')
        time.sleep(2)
