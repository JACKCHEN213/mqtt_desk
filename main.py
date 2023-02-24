# -*- coding: utf-8 -*-
import sys
import pathlib
from typing import Dict, Union
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QEvent
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QKeyEvent
from ui import MqttUi, MainUi
from config.drive import Json
from config.configuration import Configuration
from config import CONFIG_DIR, DEFAULT_CONFIG_FILE, TOPIC_CONFIG_FILE, LOG_CONFIG, VERSION
from model import MqttConfig
from utils.qt_ex import QMessageBoxEx
from utils.log import Log
from common import MQTT
from core import (
    PersistPublish,
    Publish,
    Subscribe,
    DataFormat,
    Topic
)


class Base(QMainWindow):
    def message(self, msg, title='提示', fade=1000, _type: str = 'success', auto_close=True, show_status=True):
        """
        消息提示
        :param msg: 消息内容
        :param title: 消息标题
        :param fade: 消失消失时间
        :param _type: 消息类型, [info success warning error]
        :param auto_close: 是否自动关闭
        :param show_status: 是否展示窗口，如果不展示，窗口会自动关闭
        """
        msg_box = QMessageBoxEx(parent=self)
        if not show_status:
            msg_box.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        else:
            msg_box.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        if _type.lower() == 'success':
            style = 'color: #67c23a;background-color: #f0f9eb;border-color: #e1f3d8;'
            msg_box.setIconPixmap(QPixmap(':/image/images/success_24x24.png'))
        elif _type.lower() == 'error' or _type.lower() == 'danger':
            style = 'color: #f56c6c;background-color: #fef0f0;border-color: #fde2e2;'
            msg_box.setIconPixmap(QPixmap(':/image/images/error_24x24.png'))
        elif _type.lower() == 'warning' or _type.lower() == 'warn':
            style = 'color: #e6a23c;background-color: #fdf6ec;border-color: #faecd8;'
            msg_box.setIconPixmap(QPixmap(':/image/images/warning_24x24.png'))
        else:
            style = 'color: #909399;background-color: #edf2fc;border-color: #ebeef5;'
            msg_box.setIconPixmap(QPixmap(':/image/images/info_24x24.png'))
        msg_box.setStyleSheet(style)
        msg_box.addButton('', QMessageBoxEx.AcceptRole)
        for btn in msg_box.buttons():
            btn.hide()
        msg_box.show()
        if not auto_close and show_status:
            return
        QTimer.singleShot(fade, msg_box.close)


class MqttDesk(Base):
    """
    QUESTION: MQTT连接是异步的，连接很慢时会导致界面卡顿；怎么判断mqtt是否连接成功
    SOLUTION: 将MQTT的异步连接变为同步的，根据报错信息判断是否连接成功
    """
    subscribe_render_sig: QObject = pyqtSignal(str)
    message_sig: QObject = pyqtSignal(str, str)
    set_attr_sig: QObject = pyqtSignal(QObject, str, object)

    def __init__(self, app):
        super().__init__()

        self.logger = Log('mqtt_desk', log_config=LOG_CONFIG)
        self.mqtt_config: MqttConfig = MqttConfig()
        self.subscribe_mqtt_client: Union[MQTT, None] = None
        self.publish_mqtt_client: Union[MQTT, None] = None
        self.is_subscribe = False
        self.current_subscribe = ''
        self.subscribe_text = []
        self.is_publish = False
        self.publish_thread: Union[PersistPublish, None] = None

        self.app = app
        self.main_ui = MainUi()
        self.main_ui.setupUi(self)
        self.main_mqtt_ui = QMainWindow()
        self.mqtt_ui = MqttUi()
        self.mqtt_ui.setupUi(self.main_mqtt_ui)
        self.main_mqtt_ui.setParent(self.main_ui.mqtt_tab)
        self.config_list: Dict[pathlib.Path, MqttConfig] = dict()
        self.topic_list: Dict[str, str] = {}

        self.init()
        self.set_style()
        self.set_config_list()
        self.set_topic_list()
        self.register_event()

    def init(self):
        self.main_ui.main_tab.setCurrentWidget(self.main_ui.mqtt_tab)
        self.mqtt_ui.config_load_save.setCurrentWidget(self.mqtt_ui.load_config)
        self.mqtt_ui.subscribe_publish_tab.setCurrentWidget(self.mqtt_ui.subscribe)
        self.mqtt_ui.topic.installEventFilter(self)
        self.mqtt_ui.config_list.installEventFilter(self)
        self.mqtt_ui.interval_unit.installEventFilter(self)
        self.mqtt_ui.publish_interval.setAlignment(Qt.AlignRight)
        self.mqtt_ui.config_name.setText('127.0.0.1')
        self.setFixedSize(756, 565)
        self.setWindowIcon(QIcon(':/image/images/favicon.png'))
        self.set_subscribe_text()
        self.set_status_bar()

    def set_status_bar(self):
        status_bar = self.statusBar()
        status_bar.showMessage(f'版本: {VERSION}')

    def set_subscribe_text(self):
        all_text = ''
        for index, text in enumerate(self.subscribe_text):
            all_text += "<span style='font-weight: bold;'>{:<5d}</span>{}<br />".format(index + 1, text)
        self.mqtt_ui.subscribe_text.setHtml(all_text)
        # 自动滚动
        cursor = self.mqtt_ui.subscribe_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.mqtt_ui.subscribe_text.setTextCursor(cursor)

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a0 in [self.mqtt_ui.topic, self.mqtt_ui.config_list, self.mqtt_ui.interval_unit]:
            # 别给我<Enter>自己增加item
            if a1.type() == QEvent.KeyPress:
                ke = QKeyEvent(a1)
                if ke.key() in [Qt.Key_Enter, Qt.Key_Return]:
                    return True
        return super().eventFilter(a0, a1)

    def get_save_data(self):
        return {'mqtt': self.mqtt_config.get_save_data()}

    @staticmethod
    def get_configuration_files() -> Dict[pathlib.Path, MqttConfig]:
        config_dir = pathlib.Path(CONFIG_DIR)
        config_dir.mkdir(parents=True, exist_ok=True)
        return {file: MqttConfig(**Configuration.load_config(file).get('mqtt', dict()))
                for file in list(config_dir.glob('*.ini'))}

    def set_config_list(self):
        self.config_list = self.get_configuration_files()
        if not self.config_list or '默认配置' not in [config.config_name for config in self.config_list.values()]:
            # 添加默认配置
            self.mqtt_config.config_name = '默认配置'
            default_config = pathlib.Path(CONFIG_DIR + DEFAULT_CONFIG_FILE)
            Configuration.save_config(default_config, config=self.get_save_data())
            self.config_list[default_config] = self.mqtt_config
        self.mqtt_ui.config_list.clear()
        for file, config in self.config_list.items():
            if config.config_name == '默认配置':
                self.mqtt_config = config
            self.mqtt_ui.config_list.addItem(config.config_name if config.config_name else file.stem)
        # 默认配置放在第一位
        self.mqtt_ui.config_list.setCurrentText('默认配置')
        self.set_mqtt_config()

    def set_mqtt_config(self):
        self.mqtt_ui.ip.setText(self.mqtt_config.ip.__str__())
        self.mqtt_ui.port.setText(self.mqtt_config.port.__str__())
        self.mqtt_ui.username.setText(self.mqtt_config.username.__str__())
        self.mqtt_ui.password.setText(self.mqtt_config.password.__str__())

    def load_input_config(self) -> bool:
        self.mqtt_config.ip = self.mqtt_ui.ip.text()
        try:
            self.mqtt_config.port = int(self.mqtt_ui.port.text())
        except Exception as e:
            self.logger.debug(e)
            self.message('端口类型为数字', _type='error')
            return False
        self.mqtt_config.username = self.mqtt_ui.username.text()
        self.mqtt_config.password = self.mqtt_ui.password.text()
        return True

    def set_topic_list(self):
        topic_file = pathlib.Path(CONFIG_DIR) / TOPIC_CONFIG_FILE
        if not topic_file.is_file():
            Configuration.save_config(topic_file, {'default': 'default'}, Json)
        self.topic_list = Configuration.load_config(topic_file, Json)
        if not isinstance(self.topic_list, dict):
            self.topic_list = {'default': 'default'}
            Configuration.save_config(topic_file, self.topic_list, Json)
        if self.topic_list.get('default', None) is None:
            self.topic_list['default'] = 'default'
            Configuration.save_config(topic_file, self.topic_list, Json)
        self.mqtt_ui.topic.clear()
        for topic in self.topic_list:
            self.mqtt_ui.topic.addItem(topic)
        self.mqtt_ui.topic.setCurrentText('default')
        self.mqtt_ui.publish_text.setPlainText(self.topic_list['default'])

    def __show_message(self, msg, _type):
        self.message(msg=msg, _type=_type)

    @staticmethod
    def __set_attr(obj: QObject, func: str, value: object):
        if value is None:
            getattr(obj, func)()
        else:
            getattr(obj, func)(value)

    def register_event(self):
        # 自定义信号与槽
        self.message_sig.connect(self.__show_message)
        self.set_attr_sig.connect(self.__set_attr)
        # 加载配置
        self.mqtt_ui.do_load_btn.clicked.connect(Topic.load_config(self))
        # 保存配置
        self.mqtt_ui.do_save_btn.clicked.connect(Topic.save_config(self))
        # topic保存
        self.mqtt_ui.topic_save_btn.clicked.connect(Topic.save_topic(self))
        self.mqtt_ui.topic.currentIndexChanged.connect(Topic.change_topic(self))
        # JSON
        self.mqtt_ui.json_format.clicked.connect(DataFormat.json_format(self))
        self.mqtt_ui.json_copy.clicked.connect(DataFormat.json_copy(self))
        self.mqtt_ui.json_compress.clicked.connect(DataFormat.json_compress(self))
        # 订阅
        self.mqtt_ui.subscribe_btn.clicked.connect(Subscribe.mqtt_subscribe(self))
        self.subscribe_render_sig.connect(Subscribe.render_subscribe_text(self))
        self.mqtt_ui.subscribe_save_btn.clicked.connect(Subscribe.save_subscribe(self))
        self.mqtt_ui.subscribe_clear_btn.clicked.connect(Subscribe.clear_subscribe_text(self))
        #  发布
        self.mqtt_ui.publish_btn.clicked.connect(Publish.mqtt_publish(self))
        self.mqtt_ui.persist_publish_btn.clicked.connect(Publish.persist_mqtt_publish(self))

    def set_style(self):
        pass

    def run(self):
        self.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    mqtt_desk = MqttDesk(QApplication(sys.argv))
    mqtt_desk.run()
