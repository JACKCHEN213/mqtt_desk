# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon, QFont


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.__set_window()
        self.__set_layout()

    def __set_window(self):
        self.setWindowTitle('计算机')
        self.setWindowIcon(QIcon('calculator.png'))

        self.resize(300, 400)

    def __set_layout(self):
        container = QVBoxLayout()
        text = QLabel('0你是谁')
        text.setFont(QFont('宋体',))
        container.addWidget(text)
        # text = QLineEdit('0')
        # text.setPlaceholderText('输入计算值')
        # container.addWidget(text)

        grid = QGridLayout()
        data = [
            ['%', 'CE', 'C', '<='],
            ['1/x', 'x^2', 'x^1/2', '÷'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '=']
        ]
        for index, item in enumerate(data):
            for key, value in enumerate(item):
                btn = QPushButton(value)
                btn.clicked.connect(self.__show_value)
                btn.setFixedSize(75, 45)
                grid.addWidget(btn, index, key)

        container.addLayout(grid)
        self.setLayout(container)

    @staticmethod
    def __show_value(*args):
        print(args)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    calculator = Calculator()
    calculator.show()

    sys.exit(app.exec_())
