# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSignal, QObject


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.label_text = ''
        self.__set_window()
        self.__set_layout()

    def __set_window(self):
        self.setWindowTitle('计算机')
        self.setWindowIcon(QIcon('calculator.png'))

        self.setFixedSize(300, 400)

    def __set_layout(self):
        container = QVBoxLayout()
        self.text = QLabel(self.label_text)
        self.text.setFont(QFont('宋体',))
        container.addWidget(self.text)
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
                btn.clicked.connect(self.btn_click(value))
                btn.setFixedSize(75, 45)
                grid.addWidget(btn, index, key)

        container.addLayout(grid)
        self.setLayout(container)

    def btn_click(self, value):
        def __entry():
            # FIXME: 计算器逻辑
            self.label_text += value
            self.text.setText(self.label_text)
            self.text.repaint()
        return __entry


if __name__ == '__main__':
    app = QApplication(sys.argv)

    calculator = Calculator()
    calculator.show()

    sys.exit(app.exec_())
