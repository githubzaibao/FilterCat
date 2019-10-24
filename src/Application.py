#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
from src.logview import LogFilterWidget
from src.PySide2QtScheduler import qtScheduler
import PySide2

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initData()
        self.initSize()
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout.addWidget(self.loadTabWidgets())

    def initData(self):
        pass

    def initSize(self):
        desktop = QApplication.desktop()
        self.screenWidth = desktop.width() * 0.8
        self.screenHeight = desktop.height() * 1
        print("screen width is %d height is %d" % (self.screenWidth, self.screenHeight))
        self.resize(self.screenWidth, self.screenHeight)

    def loadTabWidgets(self):
        tabWidgets = QTabWidget()
        tabWidgets.addTab(LogFilterWidget(), "Log 查看")
        return tabWidgets
        # view = QQuickWidget()
        # url = QUrl("layout/MainWindow.qml")
        # view.setSource(url)
        # view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        # # widget = QWidget.createWindowContainer(view)
        # return view



    def closeEvent(self, event:PySide2.QtGui.QCloseEvent):
        print("MainWindow close")
        event.isAccepted()

    # class MainWindow(QMainWindow):
    #     def __init__(self):
    #         ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    #         print(ROOT_DIR)
    #
    #         QMainWindow.__init__(self)
    #         view = QQuickView()
    #         url = QUrl("layout/MainWindow.qml")
    #         view.setSource(url)
    #         view.setResizeMode(QQuickView.SizeRootObjectToView)
    #         view.show()
    #         widget = QWidget.createWindowContainer(view)
    #         self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qtScheduler.initSignal()
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
