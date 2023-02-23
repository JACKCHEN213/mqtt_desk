# -*- coding: utf-8 -*-
from typing import Union

from PyQt5.Qt import QThread
from common.mqtt import MQTT
import time


class PersistPublish(QThread):
    """
    持续推送需要开启新的线程来推送
    """
    def __init__(self, mqtt_client: MQTT, topic: str, content: str, interval: int):
        super(PersistPublish, self).__init__()
        self.client = mqtt_client
        self.topic = topic
        self.content = content
        self.interval = interval
        self.is_end = False

    def run(self) -> None:
        count = 0
        while True:
            count += 1
            if count % (self.interval * 10) == 0:
                self.client.publish(self.topic, self.content)
                count = 0
            # 这个定时器是为了方便线程退出
            time.sleep(0.1)
            if self.is_end:
                break


class Publish:
    obj = None

    @classmethod
    def __validate_param(cls) -> bool:
        if not cls.obj.ui.publish_text.toPlainText():
            cls.obj.message('发布的消息内容不能为空', _type='error')
            return False
        if not cls.obj.ui.topic.currentText():
            cls.obj.message('发布的消息主题不能为空', _type='error')
            return False
        cls.obj.load_input_config()
        if not cls.obj.validate_mqtt_config():
            return False
        cls.obj.clear_mqtt_client(cls.obj.publish_mqtt_client)
        cls.obj.publish_mqtt_client = MQTT(cls.obj.mqtt_config)
        return True

    @classmethod
    def mqtt_publish(cls, obj):
        cls.obj = obj
        return cls.__mqtt_publish

    @classmethod
    def __mqtt_publish(cls):
        if cls.obj.is_publish:
            cls.obj.message('请先停止持续发布', _type='error')
            return
        if not cls.__validate_param():
            return
        cls.obj.publish_mqtt_client.publish(cls.obj.ui.topic.currentText(), cls.obj.ui.publish_text.toPlainText())

    @classmethod
    def persist_mqtt_publish(cls, obj):
        cls.obj = obj
        return cls.__persist_mqtt_publish

    @classmethod
    def __get_publish_interval(cls) -> Union[bool, int]:
        interval = int(cls.obj.ui.publish_interval.text())
        if not interval:
            cls.obj.message('发布间隔不能为0', _type='error')
            return False
        interval_unit = cls.obj.ui.interval_unit.currentText()
        if interval_unit == '时':
            interval *= 3600
        elif interval_unit == '分':
            interval += 60
        else:
            pass
        return interval

    @classmethod
    def __persist_mqtt_publish(cls):
        if cls.obj.is_publish:
            cls.obj.publish_thread.is_end = True
            # 安全退出
            cls.obj.publish_thread.quit()
            cls.obj.publish_thread.wait()
            del cls.obj.publish_thread
            cls.obj.publish_thread = None
            cls.obj.is_publish = False
            cls.obj.ui.persist_publish_btn.setText('持续发布')
            cls.obj.ui.persist_publish_btn.setStyleSheet('')
            return
        interval = cls.__get_publish_interval()
        if isinstance(interval, bool) or not cls.__validate_param():
            return
        cls.obj.publish_thread = PersistPublish(
            mqtt_client=cls.obj.publish_mqtt_client,
            topic=cls.obj.ui.topic.currentText(),
            content=cls.obj.ui.publish_text.toPlainText(),
            interval=interval
        )
        cls.obj.publish_thread.start()
        cls.obj.is_publish = True
        cls.obj.ui.persist_publish_btn.setText('持续发布中...')
        cls.obj.ui.persist_publish_btn.setStyleSheet('color: red;')
