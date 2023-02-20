# -*- coding: utf-8 -*-
import sys
import time
import pathlib
from typing import Dict
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
import pyperclip
from desk import Ui_MainWindow
from config.mqtt_configuration import MqttConfiguration
from config.drive.ini import Ini
from config import CONFIG_DIR, DEFAULT_CONFIG
from model.mqtt import MqttConfig
from utils.qt_ex import QMessageBoxEx


class Base:
    @staticmethod
    def message(parent, msg, title='提示', timeout=1000, _type: str = 'success', auto_close=True, show_status=False):
        """
        消息提示，会自动消失
        """
        msg_box = QMessageBoxEx(parent=parent)
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
        QTimer.singleShot(timeout, msg_box.close)


class MqttDesk(Base):
    def __init__(self):
        self.mqtt_config: MqttConfig = MqttConfig()

        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.main_window.setFixedSize(756, 535)
        self.ui.setupUi(self.main_window)
        self.config_list: Dict[pathlib.Path, MqttConfig] = self.get_configuration_files()

        self.init()
        self.set_config_list()
        self.register_event()
        self.set_style()

    def init(self):
        self.ui.config_box.setCurrentWidget(self.ui.load_config)
        self.ui.send_receive_box.setCurrentWidget(self.ui.subscribe)
        self.main_window.setWindowIcon(QIcon('images/favicon.png'))

    def get_save_data(self):
        return {'mqtt': self.mqtt_config.get_save_data()}

    @staticmethod
    def get_configuration_files() -> Dict[pathlib.Path, MqttConfig]:
        config_dir = pathlib.Path(CONFIG_DIR)
        config_dir.mkdir(parents=True, exist_ok=True)
        return {file: MqttConfiguration.get_config(file, Ini()) for file in list(config_dir.iterdir())}

    def set_config_list(self):
        if not self.config_list or '默认配置' not in [config.config_name for config in self.config_list.values()]:
            # 添加默认配置
            self.mqtt_config.config_name = '默认配置'
            default_config = pathlib.Path(CONFIG_DIR + DEFAULT_CONFIG)
            MqttConfiguration.set_config(default_config, config=self.get_save_data())
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
        self.mqtt_config.port = self.ui.port.text()
        self.mqtt_config.username = self.ui.username.text()
        self.mqtt_config.password = self.ui.password.text()

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
        if self.ui.send_receive_box.currentWidget().objectName() == 'publish':
            self.ui.send_receive_box.setCurrentWidget(self.ui.subscribe)
        else:
            self.ui.send_receive_box.setCurrentWidget(self.ui.publish)

    def load_config(self):
        for file, config in self.config_list.items():
            if config.config_name == self.ui.config_list.currentText():
                self.mqtt_config = config
                self.set_mqtt_config()
                return
        for file, config in self.config_list.items():
            if file.stem == self.ui.config_list.currentText():
                self.mqtt_config = config
                self.set_mqtt_config()
                return

    def save_config(self):
        self.load_input_config()
        self.mqtt_config.config_name = self.ui.config_name.text()
        filepath = pathlib.Path(CONFIG_DIR + self.ui.config_name.text() + '.ini')
        MqttConfiguration.set_config(filepath, Ini(), self.get_save_data())
        self.mqtt_config.config_file = filepath
        self.config_list = self.get_configuration_files()
        self.set_config_list()
        for file, config in self.config_list.items():
            if file != filepath:
                continue
            self.mqtt_config = config
            self.ui.config_list.setCurrentText(config.config_name)
            self.set_mqtt_config()

    def json_format(self):
        json_text = self.ui.json_content.toPlainText()
        if not json_text:
            self.ui.json_error.setStyleSheet('color: red')
            self.ui.json_error.setPlainText('请输入json文本')
            return
        try:
            json_data = json.loads(json_text)
            self.ui.json_error.setStyleSheet('color: green')
            self.ui.json_error.setPlainText('json校验成功')
            self.ui.json_content.setPlainText(json.dumps(json_data, ensure_ascii=False, indent=2))
        except Exception as e:
            self.ui.json_error.setStyleSheet('color: red')
            self.ui.json_error.setPlainText(f'不是一个有效json文本,{repr(e)}')

    def json_copy(self):
        if not self.ui.json_content.toPlainText():
            self.message(self.main_window, '内容为空，不能复制', show_status=True, _type='warning')
            return
        pyperclip.copy(self.ui.json_content.toPlainText())
        self.message(self.main_window, '成功复制到剪切板', show_status=True)

    def json_compress(self):
        if not self.ui.json_content.toPlainText():
            self.message(self.main_window, '内容为空，不能压缩', show_status=True, _type='warning')
            return
        try:
            data = json.loads(self.ui.json_content.toPlainText())
            self.ui.json_content.setPlainText(json.dumps(data, ensure_ascii=False))
            self.ui.json_error.setStyleSheet('color: green')
            self.ui.json_error.setPlainText('json压缩成功')
        except Exception as e:
            self.ui.json_error.setStyleSheet('color: red')
            self.ui.json_error.setPlainText(f'不是一个有效json文本,{repr(e)}')

    def register_event(self):
        # 切换配置存储 or 加载
        self.ui.config_switch.clicked.connect(self.switch_config)
        # 订阅 or 发布切换
        self.ui.mode_switch.clicked.connect(self.switch_mode)
        # 加载配置
        self.ui.do_load_btn.clicked.connect(self.load_config)
        # 保存配置
        self.ui.do_save_btn.clicked.connect(self.save_config)
        # JSON
        self.ui.json_format.clicked.connect(self.json_format)
        self.ui.json_copy.clicked.connect(self.json_copy)
        self.ui.json_compress.clicked.connect(self.json_compress)

    def set_style(self):
        pass

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    mqtt_desk = MqttDesk()
    mqtt_desk.run()
