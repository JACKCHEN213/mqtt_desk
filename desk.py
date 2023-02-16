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
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 10, 701, 141))
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 29, 261, 101))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.lable1 = QtWidgets.QLabel(self.formLayoutWidget)
        self.lable1.setObjectName("lable1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lable1)
        self.mqtt_ip = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.mqtt_ip.setObjectName("mqtt_ip")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.mqtt_ip)
        self.lable3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.lable3.setObjectName("lable3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lable3)
        self.mqtt_port = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.mqtt_port.setObjectName("mqtt_port")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.mqtt_port)
        self.lable4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.lable4.setObjectName("lable4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lable4)
        self.mqtt_username = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.mqtt_username.setObjectName("mqtt_username")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.mqtt_username)
        self.lable2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.lable2.setObjectName("lable2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lable2)
        self.mqtt_password = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.mqtt_password.setObjectName("mqtt_password")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.mqtt_password)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(330, 40, 111, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.load_config = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.load_config.setObjectName("load_config")
        self.verticalLayout.addWidget(self.load_config)
        self.save_config = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.save_config.setObjectName("save_config")
        self.verticalLayout.addWidget(self.save_config)
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.groupBox)
        self.stackedWidget_2.setGeometry(QtCore.QRect(460, 20, 241, 121))
        self.stackedWidget_2.setStyleSheet("background-color: rgb(52, 101, 164);")
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.widget_4 = QtWidgets.QWidget(self.page_3)
        self.widget_4.setGeometry(QtCore.QRect(0, 0, 241, 121))
        self.widget_4.setStyleSheet("background-color: rgb(92, 53, 102);")
        self.widget_4.setObjectName("widget_4")
        self.stackedWidget_2.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.widget_3 = QtWidgets.QWidget(self.page_4)
        self.widget_3.setGeometry(QtCore.QRect(0, 0, 241, 121))
        self.widget_3.setStyleSheet("background-color: rgb(204, 0, 0);")
        self.widget_3.setObjectName("widget_3")
        self.stackedWidget_2.addWidget(self.page_4)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(30, 170, 301, 281))
        self.stackedWidget.setStyleSheet("background-color: rgb(32, 74, 135);")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.widget = QtWidgets.QWidget(self.page)
        self.widget.setGeometry(QtCore.QRect(0, 0, 301, 281))
        self.widget.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.widget.setObjectName("widget")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.widget_2 = QtWidgets.QWidget(self.page_2)
        self.widget_2.setGeometry(QtCore.QRect(0, 0, 301, 281))
        self.widget_2.setStyleSheet("background-color: rgb(115, 210, 22);")
        self.widget_2.setObjectName("widget_2")
        self.stackedWidget.addWidget(self.page_2)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 460, 301, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(360, 170, 371, 341))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 300, 351, 33))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setStyleSheet("color: rgb(239, 41, 41);")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit.setGeometry(QtCore.QRect(3, 20, 368, 271))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget_2.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MQTT管理工具"))
        self.groupBox.setTitle(_translate("MainWindow", "MQTT配置"))
        self.lable1.setText(_translate("MainWindow", "MQTT主机："))
        self.mqtt_ip.setText(_translate("MainWindow", "192.168.13.76"))
        self.lable3.setText(_translate("MainWindow", "MQTT端口："))
        self.mqtt_port.setText(_translate("MainWindow", "1884"))
        self.lable4.setText(_translate("MainWindow", "登录用户："))
        self.lable2.setText(_translate("MainWindow", "登录密码："))
        self.load_config.setText(_translate("MainWindow", "加载配置"))
        self.save_config.setText(_translate("MainWindow", "保存配置"))
        self.pushButton_4.setText(_translate("MainWindow", "发布"))
        self.pushButton_5.setText(_translate("MainWindow", "订阅"))
        self.groupBox_2.setTitle(_translate("MainWindow", "JSON数据验证 && 格式化"))
        self.label.setText(_translate("MainWindow", "错误信息"))
        self.pushButton.setText(_translate("MainWindow", "格式化"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sda</p></body></html>"))
