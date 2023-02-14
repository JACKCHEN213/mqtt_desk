# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QStackedLayout,
    QPushButton,
    QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Stacked1(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel('Stacked1')
        label.setStyleSheet('color:red;')
        label.setParent(self)


class Stacked2(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel('Stacked2')
        label.setStyleSheet('color:white;background-color:red;')
        label.setParent(self)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_layout = QStackedLayout()
        self.s1 = Stacked1()
        self.s2 = Stacked2()
        self.stacked_layout.addWidget(self.s1)
        self.stacked_layout.addWidget(self.s2)

        self.__set_window()
        self.__set_layout()

    def __set_window(self):
        self.setWindowTitle('抽屉布局')

        self.resize(300, 270)

    def __set_layout(self):
        container = QVBoxLayout()

        win = QWidget()
        win.setLayout(self.stacked_layout)
        win.setStyleSheet('background-color:grey;')
        container.addWidget(win)

        btn1 = QPushButton('抽屉1')
        btn2 = QPushButton('抽屉2')
        btn1.clicked.connect(self.__btn_click1)
        btn2.clicked.connect(self.__btn_click2)
        container.addWidget(btn1)
        container.addWidget(btn2)

        self.setLayout(container)

    def __btn_click1(self):
        # self.stacked_layout.setCurrentIndex(0)
        self.stacked_layout.setCurrentWidget(self.s1)

    def __btn_click2(self):
        # self.stacked_layout.setCurrentIndex(1)
        self.stacked_layout.setCurrentWidget(self.s2)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    w.show()

    sys.exit(app.exec_())
