# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import desk


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = desk.Ui_MainWindow()
    # 固定高度
    MainWindow.setFixedSize(756, 535)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
