# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog

from common import MQTT
import json


class Subscribe:
    obj = None

    @classmethod
    def mqtt_subscribe(cls, obj):
        cls.obj = obj
        return cls.__mqtt_subscribe
    
    @classmethod
    def __receive_topic(cls, data, topic):
        """
        NOTE: 这里是在子线程中不能渲染界面，通过触发自定事件，使主线程渲染
        """
        if not isinstance(data, str):
            data = json.dumps(data)
        cls.obj.logger.debug(f'收到{topic}的消息: {data}')
        cls.obj.subscribe_render_sig.emit(data)

    @classmethod
    def __mqtt_subscribe(cls):
        if cls.obj.is_subscribe:
            if cls.obj.subscribe_mqtt_client:
                cls.obj.subscribe_mqtt_client.unsubscribe(cls.obj.current_subscribe)
            cls.obj.is_subscribe = False
            cls.obj.current_subscribe = ''
            cls.obj.ui.subscribe_btn.setText('订阅')
            cls.obj.ui.subscribe_btn.setStyleSheet('')
            return
        cls.obj.load_input_config()
        if isinstance(error := cls.obj.mqtt_config.validate_config(), str):
            cls.obj.message(error, _type='error')
            return
        topic = cls.obj.ui.topic.currentText()
        if not topic:
            cls.obj.message('订阅的topic不能为空', _type='error')
            return
        if cls.obj.subscribe_mqtt_client:
            cls.obj.subscribe_mqtt_client.disconnect()
            del cls.obj.subscribe_mqtt_client
            cls.obj.subscribe_mqtt_client = None
        try:
            cls.obj.subscribe_mqtt_client = MQTT(cls.obj.mqtt_config)
        except Exception as e:
            cls.obj.logger.error(e)
            cls.obj.message('mqtt连接失败', _type='error')
            return
        cls.obj.subscribe_mqtt_client.subscribe(topic, cls.__receive_topic)
        cls.obj.is_subscribe = True
        cls.obj.current_subscribe = topic
        cls.obj.ui.subscribe_btn.setText('取消订阅')
        cls.obj.ui.subscribe_btn.setStyleSheet('color: red;')

    @classmethod
    def render_subscribe_text(cls, obj):
        cls.obj = obj
        return cls.__render_subscribe_text

    @classmethod
    def __render_subscribe_text(cls, data: str):
        cls.obj.subscribe_text.append(data)
        cls.obj.set_subscribe_text()
    
    @classmethod
    def save_subscribe(cls, obj):
        cls.obj = obj
        return cls.__save_subscribe
    
    @classmethod
    def __save_subscribe(cls):
        if not cls.obj.subscribe_text:
            cls.obj.message('数据为空，无法保存', _type='warning')
            return
        file_name = QFileDialog.getSaveFileName(cls.obj, '保存MQTT数据', os.getcwd(),
                                                "文本文件(*.txt)", options=QFileDialog.DontUseNativeDialog)
        if not file_name[0]:
            cls.obj.message('数据保存失败，重新选择', _type='warning')
            return
        with open(file_name[0] + '.txt', 'a+') as fp:
            fp.writelines([str(text) + "\n\n" for text in cls.obj.subscribe_text])
            cls.obj.message('文件保存成功')
            cls.obj.logger.info(f'保存MQTT数据成功, {file_name[0]}.txt')
    
    @classmethod
    def clear_subscribe_text(cls, obj):
        cls.obj = obj
        return cls.__clear_subscribe_text
    
    @classmethod
    def __clear_subscribe_text(cls):
        cls.obj.subscribe_text = []
        cls.obj.set_subscribe_text()
