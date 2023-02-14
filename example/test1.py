# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDesktopWidget
from PyQt5.QtGui import QIcon

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    w.setGeometry(100, 100, 800, 800)

    label = QLabel('xxxx', w)
    label.setGeometry(0, 0, 40, 20)
    # label.setParent(w)

    btn = QPushButton('btn')
    btn.setGeometry(30, 20, 40, 40)
    btn.setParent(w)

    w.setWindowTitle('MFC app')
    print(w.frameGeometry().getCoords())
    print(w.frameGeometry().getRect())
    print(QDesktopWidget().availableGeometry())
    w.setWindowIcon(QIcon('kiss.png'))

    w.show()
    app.exec_()
