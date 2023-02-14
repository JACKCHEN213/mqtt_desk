# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QFormLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.__set_window()
        self.__set_layout()

    def __set_window(self):
        self.setWindowTitle('登录')
        self.setWindowIcon(QIcon('calculator.png'))

        self.resize(300, 150)

    def __set_layout(self):
        container = QVBoxLayout()

        form_layout = QFormLayout()
        username = QLineEdit()
        username.setPlaceholderText('请输入用户名')
        form_layout.addRow('用户名：', username)

        username = QLineEdit()
        username.setPlaceholderText('请输入密码')
        form_layout.addRow('密码：', username)
        container.addLayout(form_layout)

        btn = QPushButton('登录')
        btn.setFixedSize(100, 30)
        container.addWidget(btn, alignment=Qt.AlignRight)

        self.setLayout(container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    login = Login()
    login.show()

    sys.exit(app.exec_())
