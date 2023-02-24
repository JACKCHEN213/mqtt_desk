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
        MainWindow.resize(756, 533)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mqtt_config_box = QtWidgets.QGroupBox(self.centralwidget)
        self.mqtt_config_box.setGeometry(QtCore.QRect(30, 10, 301, 161))
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
        self.json_format_box = QtWidgets.QGroupBox(self.centralwidget)
        self.json_format_box.setGeometry(QtCore.QRect(360, 220, 371, 291))
        self.json_format_box.setObjectName("json_format_box")
        self.json_content = QtWidgets.QPlainTextEdit(self.json_format_box)
        self.json_content.setGeometry(QtCore.QRect(3, 20, 368, 231))
        self.json_content.setObjectName("json_content")
        self.json_compress = QtWidgets.QPushButton(self.json_format_box)
        self.json_compress.setGeometry(QtCore.QRect(150, 256, 61, 31))
        self.json_compress.setObjectName("json_compress")
        self.json_copy = QtWidgets.QPushButton(self.json_format_box)
        self.json_copy.setGeometry(QtCore.QRect(80, 256, 61, 31))
        self.json_copy.setObjectName("json_copy")
        self.json_format = QtWidgets.QPushButton(self.json_format_box)
        self.json_format.setGeometry(QtCore.QRect(10, 256, 61, 31))
        self.json_format.setObjectName("json_format")
        self.topic_box = QtWidgets.QGroupBox(self.centralwidget)
        self.topic_box.setGeometry(QtCore.QRect(30, 180, 301, 61))
        self.topic_box.setObjectName("topic_box")
        self.topic_label = QtWidgets.QLabel(self.topic_box)
        self.topic_label.setGeometry(QtCore.QRect(10, 30, 50, 25))
        self.topic_label.setObjectName("topic_label")
        self.topic = QtWidgets.QComboBox(self.topic_box)
        self.topic.setGeometry(QtCore.QRect(60, 30, 171, 25))
        self.topic.setEditable(True)
        self.topic.setDuplicatesEnabled(False)
        self.topic.setObjectName("topic")
        self.topic_save_btn = QtWidgets.QPushButton(self.topic_box)
        self.topic_save_btn.setGeometry(QtCore.QRect(240, 30, 51, 25))
        self.topic_save_btn.setObjectName("topic_save_btn")
        self.config_load_save = QtWidgets.QTabWidget(self.centralwidget)
        self.config_load_save.setGeometry(QtCore.QRect(370, 30, 361, 141))
        self.config_load_save.setWhatsThis("")
        self.config_load_save.setObjectName("config_load_save")
        self.load_config = QtWidgets.QWidget()
        self.load_config.setObjectName("load_config")
        self.config_list = QtWidgets.QComboBox(self.load_config)
        self.config_list.setGeometry(QtCore.QRect(10, 20, 151, 25))
        self.config_list.setEditable(True)
        self.config_list.setObjectName("config_list")
        self.do_load_btn = QtWidgets.QPushButton(self.load_config)
        self.do_load_btn.setGeometry(QtCore.QRect(180, 20, 51, 25))
        self.do_load_btn.setObjectName("do_load_btn")
        self.config_load_save.addTab(self.load_config, "")
        self.save_config = QtWidgets.QWidget()
        self.save_config.setObjectName("save_config")
        self.config_name = QtWidgets.QLineEdit(self.save_config)
        self.config_name.setGeometry(QtCore.QRect(10, 20, 151, 25))
        self.config_name.setObjectName("config_name")
        self.do_save_btn = QtWidgets.QPushButton(self.save_config)
        self.do_save_btn.setGeometry(QtCore.QRect(180, 20, 51, 25))
        self.do_save_btn.setObjectName("do_save_btn")
        self.config_load_save.addTab(self.save_config, "")
        self.subscribe_publish_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.subscribe_publish_tab.setGeometry(QtCore.QRect(30, 250, 301, 261))
        self.subscribe_publish_tab.setObjectName("subscribe_publish_tab")
        self.subscribe = QtWidgets.QWidget()
        self.subscribe.setObjectName("subscribe")
        self.subscribe_text = QtWidgets.QTextBrowser(self.subscribe)
        self.subscribe_text.setGeometry(QtCore.QRect(0, 0, 301, 198))
        self.subscribe_text.setStyleSheet("QTextBrowser {\n"
"   border: None;\n"
"   border-bottom: 1px solid #999;\n"
"}")
        self.subscribe_text.setObjectName("subscribe_text")
        self.subscribe_btn = QtWidgets.QPushButton(self.subscribe)
        self.subscribe_btn.setGeometry(QtCore.QRect(0, 200, 91, 31))
        self.subscribe_btn.setObjectName("subscribe_btn")
        self.subscribe_save_btn = QtWidgets.QPushButton(self.subscribe)
        self.subscribe_save_btn.setGeometry(QtCore.QRect(104, 200, 91, 31))
        self.subscribe_save_btn.setObjectName("subscribe_save_btn")
        self.subscribe_clear_btn = QtWidgets.QPushButton(self.subscribe)
        self.subscribe_clear_btn.setGeometry(QtCore.QRect(210, 200, 91, 31))
        self.subscribe_clear_btn.setObjectName("subscribe_clear_btn")
        self.subscribe_publish_tab.addTab(self.subscribe, "")
        self.publish = QtWidgets.QWidget()
        self.publish.setObjectName("publish")
        self.publish_btn = QtWidgets.QPushButton(self.publish)
        self.publish_btn.setGeometry(QtCore.QRect(0, 200, 91, 31))
        self.publish_btn.setStyleSheet("QPushButton:pressed {\n"
"    color: white;\n"
"    background-color: brown;\n"
"}")
        self.publish_btn.setObjectName("publish_btn")
        self.interval_unit = QtWidgets.QComboBox(self.publish)
        self.interval_unit.setGeometry(QtCore.QRect(170, 202, 41, 25))
        self.interval_unit.setStyleSheet("QComboBox::drop-down {\n"
"  image: None;\n"
"}\n"
"\n"
"QComboBox {\n"
"  border-style: None;\n"
"  color: brown;\n"
"  background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"  color: green;\n"
"  background-color: #ddd;\n"
"}")
        self.interval_unit.setObjectName("interval_unit")
        self.interval_unit.addItem("")
        self.interval_unit.addItem("")
        self.interval_unit.addItem("")
        self.interval_text1 = QtWidgets.QLabel(self.publish)
        self.interval_text1.setGeometry(QtCore.QRect(100, 202, 31, 25))
        self.interval_text1.setStyleSheet("color: brown;")
        self.interval_text1.setObjectName("interval_text1")
        self.publish_interval = QtWidgets.QLineEdit(self.publish)
        self.publish_interval.setGeometry(QtCore.QRect(130, 202, 41, 25))
        self.publish_interval.setStyleSheet("QLineEdit {\n"
"   color: brown;\n"
"   border: None;\n"
"   text-align: right\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"   color: red;\n"
"   border: 1px solid #999;\n"
"   border-radius: 5px;\n"
"}")
        self.publish_interval.setObjectName("publish_interval")
        self.persist_publish_btn = QtWidgets.QPushButton(self.publish)
        self.persist_publish_btn.setGeometry(QtCore.QRect(210, 200, 91, 31))
        self.persist_publish_btn.setObjectName("persist_publish_btn")
        self.publish_text = QtWidgets.QTextEdit(self.publish)
        self.publish_text.setGeometry(QtCore.QRect(0, 0, 301, 198))
        self.publish_text.setStyleSheet("QTextEdit {\n"
"   border: None;\n"
"   border-bottom: 1px solid #999;\n"
"}")
        self.publish_text.setObjectName("publish_text")
        self.subscribe_publish_tab.addTab(self.publish, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        self.config_load_save.setCurrentIndex(1)
        self.subscribe_publish_tab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MQTT管理工具"))
        self.mqtt_config_box.setTitle(_translate("MainWindow", "MQTT配置"))
        self.lable1.setText(_translate("MainWindow", "MQTT主机："))
        self.lable3.setText(_translate("MainWindow", "MQTT端口："))
        self.lable4.setText(_translate("MainWindow", "登录用户："))
        self.lable2.setText(_translate("MainWindow", "登录密码："))
        self.json_format_box.setTitle(_translate("MainWindow", "JSON数据验证 && 格式化"))
        self.json_compress.setText(_translate("MainWindow", "压缩"))
        self.json_copy.setText(_translate("MainWindow", "复制"))
        self.json_format.setText(_translate("MainWindow", "格式化"))
        self.topic_box.setTitle(_translate("MainWindow", "topic配置"))
        self.topic_label.setText(_translate("MainWindow", "topic："))
        self.topic_save_btn.setText(_translate("MainWindow", "保存"))
        self.load_config.setToolTip(_translate("MainWindow", "加载"))
        self.do_load_btn.setText(_translate("MainWindow", "加载"))
        self.config_load_save.setTabText(self.config_load_save.indexOf(self.load_config), _translate("MainWindow", "加载"))
        self.config_name.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.do_save_btn.setText(_translate("MainWindow", "保存"))
        self.config_load_save.setTabText(self.config_load_save.indexOf(self.save_config), _translate("MainWindow", "保存"))
        self.subscribe_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.subscribe_btn.setText(_translate("MainWindow", "订阅"))
        self.subscribe_save_btn.setText(_translate("MainWindow", "保存到文件"))
        self.subscribe_clear_btn.setText(_translate("MainWindow", "清空"))
        self.subscribe_publish_tab.setTabText(self.subscribe_publish_tab.indexOf(self.subscribe), _translate("MainWindow", "订阅"))
        self.publish_btn.setText(_translate("MainWindow", "发布"))
        self.interval_unit.setItemText(0, _translate("MainWindow", "秒"))
        self.interval_unit.setItemText(1, _translate("MainWindow", "分"))
        self.interval_unit.setItemText(2, _translate("MainWindow", "时"))
        self.interval_text1.setText(_translate("MainWindow", "间隔"))
        self.publish_interval.setText(_translate("MainWindow", "1"))
        self.persist_publish_btn.setText(_translate("MainWindow", "持续发布"))
        self.publish_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.subscribe_publish_tab.setTabText(self.subscribe_publish_tab.indexOf(self.publish), _translate("MainWindow", "发布"))
import data_rc
