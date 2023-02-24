# -*- coding: utf-8 -*-
import os
import time
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog
from common import MQTT
import json


def enable_subscribe_btn(func):
    def wrapper(cls=None):
        cls.obj.set_attr_sig.emit(cls.obj.ui.subscribe_btn, 'setEnabled', False)
        cls.obj.set_attr_sig.emit(cls.obj.ui.subscribe_btn, 'setStyleSheet', '')
        cls.obj.set_attr_sig.emit(cls.obj.ui.subscribe_btn, 'repaint', None)
        func(cls)
        cls.obj.set_attr_sig.emit(cls.obj.ui.subscribe_btn, 'setEnabled', True)
    return wrapper


class SubscribeThread(QThread):
    def __init__(self, obj, topic, callback):
        super(SubscribeThread, self).__init__()
        self.is_end = False
        self.obj = obj
        self.topic = topic
        self.callback = callback

    @enable_subscribe_btn
    def __subscribe(self):
        if self.obj.subscribe_mqtt_client:
            self.obj.subscribe_mqtt_client.disconnect()
            del self.obj.subscribe_mqtt_client
            self.obj.subscribe_mqtt_client = None
        try:
            self.obj.subscribe_mqtt_client = MQTT(self.obj.mqtt_config)
        except Exception as e:
            self.obj.logger.error(e)
            self.obj.message_sig.emit('mqtt连接失败', 'error')
            return
        self.obj.subscribe_mqtt_client.subscribe(self.topic, self.callback)
        self.obj.is_subscribe = True
        self.obj.current_subscribe = self.topic
        self.obj.set_attr_sig.emit(self.obj.ui.subscribe_btn, 'setText', '取消订阅')
        self.obj.set_attr_sig.emit(self.obj.ui.subscribe_btn, 'setStyleSheet', 'color: red')

    def run(self) -> None:
        self.__subscribe()
        while True:
            time.sleep(0.1)
            if self.is_end:
                break


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
    @enable_subscribe_btn
    def __mqtt_subscribe(cls):
        """
        订阅topic
        NOTE: 多线程订阅
        """
        if cls.obj.is_subscribe:
            if cls.obj.subscribe_mqtt_client:
                cls.obj.subscribe_mqtt_client.unsubscribe(cls.obj.current_subscribe)
            if hasattr(cls.obj, 'subscribe_thread'):
                cls.obj.subscribe_thread.is_end = True
                cls.obj.subscribe_thread.quit()
                cls.obj.subscribe_thread.wait()
                del cls.obj.subscribe_thread
            cls.obj.is_subscribe = False
            cls.obj.current_subscribe = ''
            cls.obj.set_attr_sig.emit(cls.obj.ui.subscribe_btn, 'setText', '订阅')
            cls.obj.set_attr_sig.emit(cls.obj.ui.subscribe_btn, 'setStyleSheet', '')
            return
        if not cls.obj.load_input_config():
            return
        if isinstance(error := cls.obj.mqtt_config.validate_config(), str):
            cls.obj.message_sig.emit(error, 'error')
            return
        topic = cls.obj.ui.topic.currentText()
        if not topic:
            cls.obj.message_sig.emit('订阅的topic不能为空', 'error')
            return
        cls.obj.subscribe_thread = SubscribeThread(
            obj=cls.obj,
            topic=topic,
            callback=cls.__receive_topic
        )
        cls.obj.subscribe_thread.start()

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
