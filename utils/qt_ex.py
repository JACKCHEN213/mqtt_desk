# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui


class QMessageBoxEx(QtWidgets.QMessageBox):
    def __init__(self, width=200, height=60, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__width = width
        self.__height = height

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.__width, self.__height)
