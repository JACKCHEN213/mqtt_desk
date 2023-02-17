# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'desk.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(756, 535)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mqtt_config_box = QtWidgets.QGroupBox(self.centralwidget)
        self.mqtt_config_box.setGeometry(QtCore.QRect(30, 10, 701, 161))
        self.mqtt_config_box.setObjectName("mqtt_config_box")
        self.formLayoutWidget = QtWidgets.QWidget(self.mqtt_config_box)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 29, 261, 120))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.lable1 = QtWidgets.QLabel(self.formLayoutWidget)
        self.lable1.setObjectName("lable1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lable1)
        self.ip = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ip.setText("")
        self.ip.setObjectName("ip")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ip)
        self.lable3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.lable3.setObjectName("lable3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lable3)
        self.port = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.port.setText("")
        self.port.setObjectName("port")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.port)
        self.lable4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.lable4.setObjectName("lable4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lable4)
        self.username = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.username.setObjectName("username")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.username)
        self.lable2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.lable2.setObjectName("lable2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lable2)
        self.password = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.password.setObjectName("password")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.password)
        self.config_save_load = QtWidgets.QGroupBox(self.mqtt_config_box)
        self.config_save_load.setGeometry(QtCore.QRect(320, 30, 351, 121))
        self.config_save_load.setObjectName("config_save_load")
        self.config_box = QtWidgets.QStackedWidget(self.config_save_load)
        self.config_box.setGeometry(QtCore.QRect(100, 40, 241, 61))
        self.config_box.setStyleSheet("")
        self.config_box.setObjectName("config_box")
        self.load_config = QtWidgets.QWidget()
        self.load_config.setStyleSheet("")
        self.load_config.setObjectName("load_config")
        self.config_list = QtWidgets.QComboBox(self.load_config)
        self.config_list.setGeometry(QtCore.QRect(10, 20, 151, 25))
        self.config_list.setObjectName("config_list")
        self.config_list.addItem("")
        self.do_load_btn = QtWidgets.QPushButton(self.load_config)
        self.do_load_btn.setGeometry(QtCore.QRect(170, 20, 51, 25))
        self.do_load_btn.setObjectName("do_load_btn")
        self.config_box.addWidget(self.load_config)
        self.save_config = QtWidgets.QWidget()
        self.save_config.setStyleSheet("")
        self.save_config.setObjectName("save_config")
        self.do_save_btn = QtWidgets.QPushButton(self.save_config)
        self.do_save_btn.setGeometry(QtCore.QRect(170, 20, 51, 25))
        self.do_save_btn.setObjectName("do_save_btn")
        self.config_name = QtWidgets.QLineEdit(self.save_config)
        self.config_name.setGeometry(QtCore.QRect(10, 20, 151, 25))
        self.config_name.setObjectName("config_name")
        self.config_box.addWidget(self.save_config)
        self.config_switch = QtWidgets.QPushButton(self.config_save_load)
        self.config_switch.setGeometry(QtCore.QRect(30, 58, 30, 30))
        self.config_switch.setStyleSheet("QPushButton {\n"
"    border-radius : 15px;\n"
"    background-color: #fff;\n"
"    image: url(:/image/images/switch.png);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #eee;\n"
"}\n"
"")
        self.config_switch.setText("")
        self.config_switch.setObjectName("config_switch")
        self.config_swicth_load = QtWidgets.QLabel(self.config_save_load)
        self.config_swicth_load.setGeometry(QtCore.QRect(30, 30, 31, 17))
        self.config_swicth_load.setStyleSheet("color: rgb(115, 210, 22);")
        self.config_swicth_load.setObjectName("config_swicth_load")
        self.config_swicth_save = QtWidgets.QLabel(self.config_save_load)
        self.config_swicth_save.setGeometry(QtCore.QRect(30, 94, 31, 17))
        self.config_swicth_save.setObjectName("config_swicth_save")
        self.send_receive_box = QtWidgets.QStackedWidget(self.centralwidget)
        self.send_receive_box.setGeometry(QtCore.QRect(30, 240, 301, 271))
        self.send_receive_box.setStyleSheet("")
        self.send_receive_box.setObjectName("send_receive_box")
        self.publish = QtWidgets.QWidget()
        self.publish.setStyleSheet("")
        self.publish.setObjectName("publish")
        self.publish_text = QtWidgets.QTextEdit(self.publish)
        self.publish_text.setGeometry(QtCore.QRect(0, 0, 301, 231))
        self.publish_text.setObjectName("publish_text")
        self.publish_btn = QtWidgets.QPushButton(self.publish)
        self.publish_btn.setGeometry(QtCore.QRect(10, 236, 91, 31))
        self.publish_btn.setObjectName("publish_btn")
        self.send_receive_box.addWidget(self.publish)
        self.subscribe = QtWidgets.QWidget()
        self.subscribe.setStyleSheet("")
        self.subscribe.setObjectName("subscribe")
        self.subscribe_text = QtWidgets.QTextBrowser(self.subscribe)
        self.subscribe_text.setGeometry(QtCore.QRect(0, 0, 301, 231))
        self.subscribe_text.setObjectName("subscribe_text")
        self.subscribe_btn = QtWidgets.QPushButton(self.subscribe)
        self.subscribe_btn.setGeometry(QtCore.QRect(10, 236, 91, 31))
        self.subscribe_btn.setObjectName("subscribe_btn")
        self.subscribe_btn_2 = QtWidgets.QPushButton(self.subscribe)
        self.subscribe_btn_2.setGeometry(QtCore.QRect(110, 236, 91, 31))
        self.subscribe_btn_2.setObjectName("subscribe_btn_2")
        self.send_receive_box.addWidget(self.subscribe)
        self.json_format_box = QtWidgets.QGroupBox(self.centralwidget)
        self.json_format_box.setGeometry(QtCore.QRect(360, 180, 371, 331))
        self.json_format_box.setObjectName("json_format_box")
        self.json_content = QtWidgets.QPlainTextEdit(self.json_format_box)
        self.json_content.setGeometry(QtCore.QRect(3, 20, 368, 221))
        self.json_content.setObjectName("json_content")
        self.json_compress = QtWidgets.QPushButton(self.json_format_box)
        self.json_compress.setGeometry(QtCore.QRect(310, 300, 61, 31))
        self.json_compress.setObjectName("json_compress")
        self.json_copy = QtWidgets.QPushButton(self.json_format_box)
        self.json_copy.setGeometry(QtCore.QRect(310, 270, 61, 31))
        self.json_copy.setObjectName("json_copy")
        self.json_format = QtWidgets.QPushButton(self.json_format_box)
        self.json_format.setGeometry(QtCore.QRect(310, 240, 61, 31))
        self.json_format.setObjectName("json_format")
        self.json_error = QtWidgets.QTextBrowser(self.json_format_box)
        self.json_error.setGeometry(QtCore.QRect(10, 246, 291, 81))
        self.json_error.setStyleSheet("color: rgb(115, 210, 22);")
        self.json_error.setObjectName("json_error")
        self.topic_box = QtWidgets.QGroupBox(self.centralwidget)
        self.topic_box.setGeometry(QtCore.QRect(30, 180, 241, 61))
        self.topic_box.setObjectName("topic_box")
        self.topic_label = QtWidgets.QLabel(self.topic_box)
        self.topic_label.setGeometry(QtCore.QRect(10, 30, 50, 25))
        self.topic_label.setObjectName("topic_label")
        self.topic = QtWidgets.QComboBox(self.topic_box)
        self.topic.setGeometry(QtCore.QRect(60, 30, 171, 25))
        self.topic.setObjectName("topic")
        self.topic.addItem("")
        self.topic.addItem("")
        self.mode_switch = QtWidgets.QPushButton(self.centralwidget)
        self.mode_switch.setGeometry(QtCore.QRect(280, 212, 51, 21))
        self.mode_switch.setObjectName("mode_switch")
        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        self.config_box.setCurrentIndex(1)
        self.send_receive_box.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MQTT管理工具"))
        self.mqtt_config_box.setTitle(_translate("MainWindow", "MQTT配置"))
        self.lable1.setText(_translate("MainWindow", "MQTT主机："))
        self.lable3.setText(_translate("MainWindow", "MQTT端口："))
        self.lable4.setText(_translate("MainWindow", "登录用户："))
        self.lable2.setText(_translate("MainWindow", "登录密码："))
        self.config_save_load.setTitle(_translate("MainWindow", "配置存储 && 加载"))
        self.config_list.setItemText(0, _translate("MainWindow", "默认配置"))
        self.do_load_btn.setText(_translate("MainWindow", "加载"))
        self.do_save_btn.setText(_translate("MainWindow", "保存"))
        self.config_name.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.config_swicth_load.setText(_translate("MainWindow", "加载"))
        self.config_swicth_save.setText(_translate("MainWindow", "保存"))
        self.publish_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">{&quot;&quot;}</p></body></html>"))
        self.publish_btn.setText(_translate("MainWindow", "发布"))
        self.subscribe_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">dsa</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ad</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sa</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">das</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">d</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">asd</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">asd</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sa</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">dsa</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">dsa</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">dsa</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">dsa</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">d</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sad</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sa</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">dsa</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">dsa</p></body></html>"))
        self.subscribe_btn.setText(_translate("MainWindow", "订阅"))
        self.subscribe_btn_2.setText(_translate("MainWindow", "保存到文件"))
        self.json_format_box.setTitle(_translate("MainWindow", "JSON数据验证 && 格式化"))
        self.json_compress.setText(_translate("MainWindow", "压缩"))
        self.json_copy.setText(_translate("MainWindow", "复制"))
        self.json_format.setText(_translate("MainWindow", "格式化"))
        self.json_error.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">提示信息</p></body></html>"))
        self.topic_box.setTitle(_translate("MainWindow", "topic配置"))
        self.topic_label.setText(_translate("MainWindow", "topic："))
        self.topic.setItemText(0, _translate("MainWindow", "/LocXYZ/#"))
        self.topic.setItemText(1, _translate("MainWindow", "..."))
        self.mode_switch.setText(_translate("MainWindow", "切换"))
import data_rc
