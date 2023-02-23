# -*- coding: utf-8 -*-
import sys
import time
import pathlib
from typing import Dict, Union
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QEvent
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QKeyEvent
from desk import Ui_MainWindow
from config.drive import Json
from config.configuration import Configuration
from config import CONFIG_DIR, DEFAULT_CONFIG_FILE, TOPIC_CONFIG_FILE, LOG_CONFIG
from model import MqttConfig, MultiCssModel
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
            msg_box.setIconPixmap(QPixmap('images/success_24x24.png'))
        elif _type.lower() == 'error' or _type.lower() == 'danger':
            style = 'color: #f56c6c;background-color: #fef0f0;border-color: #fde2e2;'
            msg_box.setIconPixmap(QPixmap('images/error_24x24.png'))
        elif _type.lower() == 'warning' or _type.lower() == 'warn':
            style = 'color: #e6a23c;background-color: #fdf6ec;border-color: #faecd8;'
            msg_box.setIconPixmap(QPixmap('images/warning_24x24.png'))
        else:
            style = 'color: #909399;background-color: #edf2fc;border-color: #ebeef5;'
            msg_box.setIconPixmap(QPixmap('images/info_24x24.png'))
        msg_box.setStyleSheet(style)
        msg_box.addButton('', QMessageBoxEx.AcceptRole)
        for btn in msg_box.buttons():
            btn.hide()
        msg_box.show()
        if not auto_close and show_status:
            return
        QTimer.singleShot(fade, msg_box.close)


class MqttDesk(Base):
    subscribe_render_sig: QObject = pyqtSignal(str)

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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config_list: Dict[pathlib.Path, MqttConfig] = dict()
        self.topic_list: Dict[str, str] = {}

        self.init()
        self.set_style()
        self.set_config_list()
        self.set_topic_list()
        self.register_event()

    def init(self):
        self.ui.config_box.setCurrentWidget(self.ui.load_config)
        self.ui.send_receive_box.setCurrentWidget(self.ui.subscribe)
        self.ui.topic.installEventFilter(self)
        self.ui.config_list.installEventFilter(self)
        self.ui.interval_unit.installEventFilter(self)
        self.ui.publish_interval.setAlignment(Qt.AlignRight)
        self.setFixedSize(756, 535)
        self.setWindowIcon(QIcon('images/favicon.png'))
        self.set_subscribe_text()

    def set_subscribe_text(self):
        all_text = ''
        for index, text in enumerate(self.subscribe_text):
            all_text += "<span style='font-weight: bold;'>{:<5d}</span>{}<br />".format(index + 1, text)
        self.ui.subscribe_text.setHtml(all_text)
        # 自动滚动
        cursor = self.ui.subscribe_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.ui.subscribe_text.setTextCursor(cursor)

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a0 in [self.ui.topic, self.ui.config_list, self.ui.interval_unit]:
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
        self.ui.config_list.clear()
        for file, config in self.config_list.items():
            if config.config_name == '默认配置':
                self.mqtt_config = config
            self.ui.config_list.addItem(config.config_name if config.config_name else file.stem)
        # 默认配置放在第一位
        self.ui.config_list.setCurrentText('默认配置')
        self.set_mqtt_config()

    def set_mqtt_config(self):
        self.ui.ip.setText(self.mqtt_config.ip.__str__())
        self.ui.port.setText(self.mqtt_config.port.__str__())
        self.ui.username.setText(self.mqtt_config.username.__str__())
        self.ui.password.setText(self.mqtt_config.password.__str__())

    def load_input_config(self):
        self.mqtt_config.ip = self.ui.ip.text()
        self.mqtt_config.port = int(self.ui.port.text())
        self.mqtt_config.username = self.ui.username.text()
        self.mqtt_config.password = self.ui.password.text()

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
        self.ui.topic.clear()
        for topic in self.topic_list:
            self.ui.topic.addItem(topic)
        self.ui.topic.setCurrentText('default')
        self.ui.publish_text.setPlainText(self.topic_list['default'])

    def switch_config(self):
        """
        配置存储 or 加载切换
        """
        style_sheet = "color: rgb(115, 210, 22);"
        if self.ui.config_box.currentWidget().objectName() == 'load_config':
            self.ui.config_swicth_load.setStyleSheet('')
            self.ui.config_swicth_save.setStyleSheet(style_sheet)
            self.ui.config_box.setCurrentWidget(self.ui.save_config)
            self.ui.config_name.setText(str(int(time.time())))
        else:
            self.ui.config_swicth_load.setStyleSheet(style_sheet)
            self.ui.config_swicth_save.setStyleSheet('')
            self.ui.config_box.setCurrentWidget(self.ui.load_config)

    def switch_mode(self):
        """
        订阅 or 发布切换
        """
        color = 'green'
        text = '订阅模式'
        if self.ui.send_receive_box.currentWidget().objectName() == 'publish':
            self.ui.send_receive_box.setCurrentWidget(self.ui.subscribe)
        else:
            self.ui.send_receive_box.setCurrentWidget(self.ui.publish)
            color = 'brown'
            text = '发布模式'
        self.mode_switch_style.data['QPushButton'].attrs['image'] =\
            f'url(:/image/images/mode_switch_{color}_32x32.png)'
        self.ui.mode_switch.setStyleSheet(self.mode_switch_style.__str__())
        self.mode_switch_text_style.data['QLabel'].attrs['color'] = color
        self.ui.mode_switch_text.setStyleSheet(self.mode_switch_text_style.__str__())
        self.ui.mode_switch_text.setText(text)

    def register_event(self):
        # 切换配置存储 or 加载
        self.ui.config_switch.clicked.connect(self.switch_config)
        # 订阅 or 发布切换
        self.ui.mode_switch.clicked.connect(self.switch_mode)
        # 加载配置
        self.ui.do_load_btn.clicked.connect(Topic.load_config(self))
        # 保存配置
        self.ui.do_save_btn.clicked.connect(Topic.save_config(self))
        # topic保存
        self.ui.topic_save_btn.clicked.connect(Topic.save_topic(self))
        self.ui.topic.currentIndexChanged.connect(Topic.change_topic(self))
        # JSON
        self.ui.json_format.clicked.connect(DataFormat.json_format(self))
        self.ui.json_copy.clicked.connect(DataFormat.json_copy(self))
        self.ui.json_compress.clicked.connect(DataFormat.json_compress(self))
        # 订阅
        self.ui.subscribe_btn.clicked.connect(Subscribe.mqtt_subscribe(self))
        self.subscribe_render_sig.connect(Subscribe.render_subscribe_text(self))
        self.ui.subscribe_save_btn.clicked.connect(Subscribe.save_subscribe(self))
        self.ui.subscribe_clear_btn.clicked.connect(Subscribe.clear_subscribe_text(self))
        #  发布
        self.ui.publish_btn.clicked.connect(Publish.mqtt_publish(self))
        self.ui.persist_publish_btn.clicked.connect(Publish.persist_mqtt_publish(self))

    def set_style(self):
        # TODO: 样式需要统一管理
        self.mode_switch_style = MultiCssModel()
        self.mode_switch_style.data['QPushButton'] = MultiCssModel.single_class()(
            tag_name='QPushButton',
            border_radius='14px',
            background_color='#eee',
            image='url(:/image/images/mode_switch_green_32x32.png)'
        )
        self.mode_switch_style.data['QPushButton:hover'] = MultiCssModel.single_class()(
            tag_name='QPushButton:hover',
            background_color='#ddd',
        )
        self.mode_switch_text_style = MultiCssModel()
        self.mode_switch_text_style.data['QLabel'] = MultiCssModel.single_class()(
            tag_name='QLabel',
            color='green'
        )

    def run(self):
        self.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    mqtt_desk = MqttDesk(QApplication(sys.argv))
    mqtt_desk.run()
