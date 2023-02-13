# -*- coding: utf-8 -*-
import os
import sys
os.chdir(os.path.abspath(os.path.dirname(__file__) + '/../..'))
sys.path.append('.')
from common.mqtt import MQTT
from config.mqtt_configuration import MqttConfiguration
from config import CONFIG_DIR
import time


if __name__ == '__main__':
    mqtt_client = MQTT.get_instance((MqttConfiguration.get_config(CONFIG_DIR + 'default.ini')))
    while True:
        mqtt_client.publish('/test', 'hello')
        time.sleep(2)
