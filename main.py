# -*- coding: utf-8 -*-
import os
import sys
import time
import pathlib
from typing import Dict, Union
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor
import pyperclip
from desk import Ui_MainWindow
from config.mqtt_configuration import MqttConfiguration
from config.drive.ini import Ini
from config import CONFIG_DIR, DEFAULT_CONFIG
from model.mqtt import MqttConfig
from utils.qt_ex import QMessageBoxEx
from utils.log import Log
from common.mqtt import MQTT


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

        self.logger = Log('mqtt_desk')
        self.mqtt_config: MqttConfig = MqttConfig()
        self.__mqtt_client: Union[MQTT, None] = None
        self.is_subscribe = False
        self.current_subscribe = ''
        self.subscribe_text = []
        self.is_publish = False
        self.current_publish = ''
        self.publish_text = '{}'

        self.app = app
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config_list: Dict[pathlib.Path, MqttConfig] = self.get_configuration_files()

        self.init()
        self.set_config_list()
        self.register_event()
        self.set_style()

    def __set_subscribe_text(self):
        all_text = ''
        for index, text in enumerate(self.subscribe_text):
            all_text += "<span style='font-weight: bold;'>{:<5d}</span>{}<br />".format(index + 1, text)
        self.ui.subscribe_text.setHtml(all_text)
        # 自动滚动
        cursor = self.ui.subscribe_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.ui.subscribe_text.setTextCursor(cursor)

    def __set_publish_text(self):
        self.ui.publish_text.setPlainText(self.publish_text)

    def init(self):
        self.ui.config_box.setCurrentWidget(self.ui.load_config)
        self.ui.send_receive_box.setCurrentWidget(self.ui.subscribe)
        self.setFixedSize(756, 535)
        self.setWindowIcon(QIcon('images/favicon.png'))
        self.__set_subscribe_text()
        self.__set_publish_text()

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
        self.mqtt_config.port = int(self.ui.port.text())
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
            self.message('内容为空，不能复制', show_status=True, _type='warning')
            return
        pyperclip.copy(self.ui.json_content.toPlainText())
        self.message('成功复制到剪切板', show_status=True)

    def json_compress(self):
        if not self.ui.json_content.toPlainText():
            self.message('内容为空，不能压缩', show_status=True, _type='warning')
            return
        try:
            data = json.loads(self.ui.json_content.toPlainText())
            self.ui.json_content.setPlainText(json.dumps(data, ensure_ascii=False))
            self.ui.json_error.setStyleSheet('color: green')
            self.ui.json_error.setPlainText('json压缩成功')
        except Exception as e:
            self.ui.json_error.setStyleSheet('color: red')
            self.ui.json_error.setPlainText(f'不是一个有效json文本,{repr(e)}')

    def __compare_config(self):
        """
        比较配置信息，如果相同，就将连接配置应用到当前配置中
        """
        if self.mqtt_config == self.__mqtt_client.mqtt_config:
            self.mqtt_config = self.__mqtt_client.mqtt_config
            self.set_mqtt_config()
            return True
        return False

    @property
    def mqtt_client(self) -> MQTT:
        if self.__mqtt_client is None:
            self.__mqtt_client = MQTT(self.mqtt_config)
        if not self.__compare_config():
            if self.is_subscribe:
                self.__mqtt_client.unsubscribe(self.current_subscribe)
            self.__mqtt_client.client.loop_stop()
            self.__mqtt_client.client.disconnect()
            del self.__mqtt_client
            self.__mqtt_client = MQTT(self.mqtt_config)
        return self.__mqtt_client

    def clear_mqtt_client(self):
        if self.__mqtt_client is None:
            self.is_subscribe = False
            self.current_subscribe = ''
            return
        self.mqtt_client.unsubscribe(self.current_subscribe)
        self.__mqtt_client.client.loop_stop()
        self.__mqtt_client.client.disconnect()
        del self.__mqtt_client
        self.__mqtt_client = None
        self.is_subscribe = False
        self.current_subscribe = ''

    def render_subscribe_text(self, data: str):
        self.subscribe_text.append(data)
        self.__set_subscribe_text()

    def receive_topic(self, data, topic):
        """
        NOTE: 这里是在子线程中不能渲染界面，通过触发自定事件，使主线程渲染
        """
        if not isinstance(data, str):
            data = json.dumps(data)
        self.logger.debug(f'收到{topic}的消息: {data}')
        self.subscribe_render_sig.emit(data)

    def validate_ip(self) -> bool:
        ips = self.mqtt_config.ip.split('.')
        if len(ips) != 4:
            self.message('ip地址位数非法', _type='error')
            return False
        for ip in ips:
            if ip != str(int(ip)):
                self.message(f'ip段内容{ip}错误', _type='error')
                return False
            if 0 > int(ip) or int(ip) > 255:
                self.message(f'ip段长度{ip}错误', _type='error')
                return False
        return True

    def validate_mqtt_config(self) -> bool:
        if not self.mqtt_config.ip:
            self.message('mqtt的主机必须', _type='error')
            return False
        if not self.validate_ip():
            return False
        if not self.mqtt_config.port:
            self.message('mqtt的端口必须', _type='error')
            return False
        if 0 > self.mqtt_config.port or self.mqtt_config.port > 65536:
            self.message('mqtt的端口错误', _type='error')
            return False
        return True

    def mqtt_subscribe(self):
        if self.is_subscribe:
            self.clear_mqtt_client()
            self.ui.subscribe_btn.setText('订阅')
            self.ui.subscribe_btn.setStyleSheet('')
            return
        self.load_input_config()
        if not self.validate_mqtt_config():
            return
        if not self.ui.topic.currentText():
            self.message('订阅的topic不能为空', _type='error')
            return
        self.mqtt_client.subscribe('test', self.receive_topic)
        self.is_subscribe = True
        self.current_subscribe = 'test'
        self.ui.subscribe_btn.setText('取消订阅')
        self.ui.subscribe_btn.setStyleSheet('color: red;')

    def save_subscribe(self):
        if not self.subscribe_text:
            self.message('数据为空，无法保存', _type='warning')
            return
        file_name = QFileDialog.getSaveFileName(self, '保存监听文件', os.getcwd(),
                                                "文本文件(*.txt)", options=QFileDialog.DontUseNativeDialog)
        if not file_name[0]:
            self.message('数据保存失败，重新选择', _type='warning')
            return
        with open(file_name[0] + '.txt', 'a+') as fp:
            fp.writelines([str(text) + "\n\n" for text in self.subscribe_text])
            self.message('文件保存成功')

    def clear_subscribe_text(self):
        self.subscribe_text = []
        self.__set_subscribe_text()

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
        # 订阅 or 发布
        self.ui.subscribe_btn.clicked.connect(self.mqtt_subscribe)
        self.subscribe_render_sig.connect(self.render_subscribe_text)
        self.ui.subscribe_save_btn.clicked.connect(self.save_subscribe)
        self.ui.subscribe_clear_btn.clicked.connect(self.clear_subscribe_text)

    def set_style(self):
        pass

    def run(self):
        self.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    mqtt_desk = MqttDesk(QApplication(sys.argv))
    mqtt_desk.run()
