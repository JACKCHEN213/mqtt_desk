# -*- coding: utf-8 -*-
from typing import Union
from PyQt5.Qt import QThread, QObject
from PyQt5.QtCore import Qt

from common.mqtt import MQTT
import time
from utils import Log


def enable_publish_btn(func):
    def wrapper(cls=None):
        cls.obj.set_attr_sig.emit(cls.obj.ui.publish_btn, 'setEnabled', False)
        cls.obj.set_attr_sig.emit(cls.obj.ui.publish_btn, 'repaint', None)
        cls.obj.set_attr_sig.emit(cls.obj.ui.publish_btn, 'setFocus', None)
        ret = func(cls)
        cls.obj.set_attr_sig.emit(cls.obj.ui.publish_btn, 'setEnabled', True)
        cls.obj.set_attr_sig.emit(cls.obj.ui.publish_btn, 'setFocus', None)
        return ret
    return wrapper


def enable_persist_publish_btn(func):
    def wrapper(cls=None):
        cls.obj.set_attr_sig.emit(cls.obj.ui.persist_publish_btn, 'setEnabled', False)
        cls.obj.set_attr_sig.emit(cls.obj.ui.persist_publish_btn, 'setStyleSheet', '')
        cls.obj.set_attr_sig.emit(cls.obj.ui.persist_publish_btn, 'repaint', None)
        ret = func(cls)
        cls.obj.set_attr_sig.emit(cls.obj.ui.persist_publish_btn, 'setEnabled', True)
        return ret
    return wrapper


class BasePublish(QThread):
    obj: Union[None, QObject] = None

    def __init__(self, obj):
        super(BasePublish, self).__init__()
        self.obj = obj
        self.is_end = False

    def _validate_param(self) -> bool:
        if not self.obj.ui.publish_text.toPlainText():
            self.obj.message_sig.emit('发布的消息内容不能为空', 'error')
            return False
        if not self.obj.ui.topic.currentText():
            self.obj.message_sig.emit('发布的消息主题不能为空', 'error')
            return False
        if not self.obj.load_input_config():
            return False
        if isinstance(error := self.obj.mqtt_config.validate_config(), str):
            self.obj.message_sig.emit(error, 'error')
            return False
        if self.obj.publish_mqtt_client is None or self.obj.publish_mqtt_client.mqtt_config != self.obj.mqtt_config:
            # 配置发生变化才重连
            if self.obj.publish_mqtt_client:
                self.obj.publish_mqtt_client.disconnect()
                del self.obj.publish_mqtt_client
                self.obj.publish_mqtt_client = None
            try:
                self.obj.publish_mqtt_client = MQTT(self.obj.mqtt_config)
            except Exception as e:
                self.obj.logger.error(e)
                self.obj.message_sig.emit('mqtt连接失败', 'error')
                return False
        return True

    def run(self) -> None:
        pass


class PersistPublish(BasePublish):
    """
    持续推送需要开启新的线程来推送
    """
    def __get_publish_interval(self) -> Union[bool, int]:
        interval = int(self.obj.ui.publish_interval.text())
        if not interval:
            self.obj.message_sig.emit('发布间隔不能为0', 'error')
            return False
        interval_unit = self.obj.ui.interval_unit.currentText()
        if interval_unit == '时':
            interval *= 3600
        elif interval_unit == '分':
            interval += 60
        else:
            pass
        return interval

    @enable_persist_publish_btn
    def __get_params(self) -> (MQTT, str, str, int, Log, bool):
        interval = self.__get_publish_interval()
        if isinstance(interval, bool) or not self._validate_param():
            return None, None, None, None, None, True
        self.obj.is_publish = True
        self.obj.set_attr_sig.emit(self.obj.ui.persist_publish_btn, 'setText', '持续发布中...')
        self.obj.set_attr_sig.emit(self.obj.ui.persist_publish_btn, 'setStyleSheet', 'color: red;')
        self.obj.logger.info(f'持续发布中，{self.obj.mqtt_config.__str__()}，{self.obj.ui.topic.currentText()}')
        return (
            self.obj.publish_mqtt_client,
            self.obj.ui.topic.currentText(),
            self.obj.ui.publish_text.toPlainText(),
            interval,
            self.obj.logger,
            True
                )

    def run(self) -> None:
        client, topic, content, interval, logger, error = self.__get_params()
        if error:
            return
        count = 0
        while True:
            count += 1
            if count % (interval * 10) == 0:
                client.publish(topic, content)
                logger.debug(f'{topic}: {content}')
                count = 0
            # 这个定时器是为了方便线程退出
            time.sleep(0.1)
            if self.is_end:
                break


class SinglePublish(BasePublish):
    @enable_publish_btn
    def __publish(self):
        if not self._validate_param():
            return False
        self.obj.publish_mqtt_client.publish(self.obj.ui.topic.currentText(), self.obj.ui.publish_text.toPlainText())
        self.obj.logger.debug(f'{self.obj.ui.topic.currentText()}: {self.obj.ui.publish_text.toPlainText()}')
        return True
        
    def run(self) -> None:
        if not self.__publish():
            return
        while True:
            time.sleep(0.1)
            if self.is_end:
                break


class Publish:
    obj = None

    @classmethod
    def mqtt_publish(cls, obj):
        cls.obj = obj
        return cls.__mqtt_publish

    @classmethod
    @enable_publish_btn
    def __mqtt_publish(cls):
        if cls.obj.is_publish:
            cls.obj.message_sig.emit('请先停止持续发布', 'error')
            return
        if hasattr(cls.obj, 'single_publish_thread'):
            cls.obj.single_publish_thread.is_end = True
            cls.obj.single_publish_thread.quit()
            cls.obj.single_publish_thread.wait()
        cls.obj.single_publish_thread = SinglePublish(cls.obj)
        cls.obj.single_publish_thread.start()

    @classmethod
    def persist_mqtt_publish(cls, obj):
        cls.obj = obj
        return cls.__persist_mqtt_publish

    @classmethod
    @enable_persist_publish_btn
    def __persist_mqtt_publish(cls):
        if cls.obj.is_publish:
            cls.obj.publish_thread.is_end = True
            # 安全退出
            cls.obj.publish_thread.quit()
            cls.obj.publish_thread.wait()
            del cls.obj.publish_thread
            cls.obj.publish_thread = None
            cls.obj.is_publish = False
            cls.obj.set_attr_sig.emit(cls.obj.ui.persist_publish_btn, 'setText', '持续发布')
            cls.obj.set_attr_sig.emit(cls.obj.ui.persist_publish_btn, 'setStyleSheet', '')
            cls.obj.logger.info(f'持续发布结束，{cls.obj.mqtt_config.__str__()}，{cls.obj.ui.topic.currentText()}')
            return
        cls.obj.publish_thread = PersistPublish(obj=cls.obj)
        cls.obj.publish_thread.start()
