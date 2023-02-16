# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import pyqtSignal, QObject, Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.result = 0
        self.sign = ''
        self.error = ''
        self.__set_window()
        self.__set_layout()

    def __set_window(self):
        self.setWindowTitle('计算机')
        self.setWindowIcon(QIcon('calculator.png'))

        self.setFixedSize(300, 300)

    def __set_layout(self):
        container = QVBoxLayout()
        self.label = QLabel(self.result.__str__())
        self.label.setFont(QFont('宋体', 18))
        container.addWidget(self.label)
        self.error_label = QLabel(self.error)
        self.error_label.setStyleSheet('color: red')
        container.addWidget(self.error_label)
        # text = QLineEdit('0')
        # text.setPlaceholderText('输入计算值')
        # container.addWidget(text)

        grid = QGridLayout()
        data = [
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['=', '0', 'C', '÷']
        ]
        for index, item in enumerate(data):
            for key, value in enumerate(item):
                btn = QPushButton(value)
                btn.clicked.connect(self.btn_click(value))
                btn.setFixedSize(75, 45)
                grid.addWidget(btn, index, key)

        container.addLayout(grid)
        self.setLayout(container)

    def render_result(self):
        self.label.setText(self.result.__str__() + (self.sign if self.sign else ''))
        self.label.repaint()
        self.error_label.setText(self.error)
        self.error = ''
        self.error_label.repaint()

    def cal_number(self, num: int):
        if self.sign:
            if self.sign == '+':
                self.add(num)
            elif self.sign == '-':
                self.minus(num)
            elif self.sign == 'x':
                self.multiply(num)
            elif self.sign == '÷':
                self.divide(num)
            else:
                pass
            self.sign = ''
        else:
            if self.result:
                self.result = self.result * 10 + num
            else:
                self.result = num

    def add(self, num: int):
        self.result += num

    def minus(self, num: int):
        self.result -= num

    def multiply(self, num: int):
        self.result *= num

    def divide(self, num: int):
        if num == 0:
            self.result = 0
            self.error = '除零错误'
        else:
            self.result /= num

    def btn_click(self, value):
        def __entry():
            if value in [str(val) for val in range(10)]:
                self.cal_number(int(value))
            elif value == '=':
                self.sign = ''
            elif value == 'C':
                self.sign = ''
                self.result = 0
            else:
                self.sign = value
            self.render_result()
        return __entry


if __name__ == '__main__':
    app = QApplication(sys.argv)

    calculator = Calculator()
    calculator.show()

    sys.exit(app.exec_())
