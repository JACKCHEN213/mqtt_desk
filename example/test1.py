# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()

    w.setWindowTitle('MFC app')

    w.show()
    app.exec_()
