#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QLineEdit, QPushButton, QPlainTextEdit, \
    QErrorMessage
from PySide2 import QtCore
import os
from .EditWidget import EditWidget
from rxbus.core import RxBus
from src.BusData import Class
from rx import operators as ops, scheduler
from src.PySide2QtScheduler import qtScheduler
import PySide2
import rx
from src.core import Fiter


class LogFilterWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._initUI()
        self._initData()

    def _initUI(self):
        self.mainLayout = QHBoxLayout(self)
        # self.treeModel = QFileSystemModel(self)
        # self.treeView = QTreeView(self)
        self.setAcceptDrops(True)
        #
        # self.treeView.setModel(self.treeModel)
        # self.treeView.setSortingEnabled(True)
        # self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        # self.mainLayout.addWidget(self.treeView)
        self.editTabsView = QTabWidget(self)
        self.editTabsView.setTabsClosable(True)
        self.editTabsView.setMovable(True)
        self.editTabsView.setDocumentMode(True)
        self.editTabsView.tabCloseRequested.connect(self.tabCloseRequested)
        self.contentLayout = QVBoxLayout(self)
        self.topHandlerLayout = QHBoxLayout(self)
        self.input = QLineEdit(self)
        self.searchButton = QPushButton(self)
        self.searchButton.clicked.connect(self.handerFilter)
        self.searchButton.setText("搜索当前文件")

        self.searchButtonAll = QPushButton(self)
        self.searchButtonAll.clicked.connect(self.handerFilterAll)
        self.searchButtonAll.setText("搜索全部文件")

        self.topHandlerLayout.addWidget(self.input, 1)
        self.topHandlerLayout.addWidget(self.searchButton)
        self.topHandlerLayout.addWidget(self.searchButtonAll)

        self.contentLayout.addLayout(self.topHandlerLayout)

        self.contentLayout.addWidget(self.editTabsView, 1)
        self.mainLayout.addLayout(self.contentLayout, 1)
        self.setLayout(self.mainLayout)
        self._initMenus()
        RxBus.instance.register(self, Class.LogInfo).pipe(
            ops.subscribe_on(scheduler.ThreadPoolScheduler()),
            qtScheduler.QtScheduler()
        ).subscribe(
            on_next=lambda value: self.handlerLogInfo(value)
        )

    def handerFilterAll(self):
        self.startFilter(-1)

    def handerFilter(self):
        self.startFilter(self.editTabsView.currentIndex())

    def startFilter(self, index):
        searchTag = self.input.displayText()
        print(searchTag)
        filterData = list()
        if index == -1:
            print("全部")
            for i in range(self.editTabsView.count()):
                currentTab = self.editTabsView.widget(i)
                data = currentTab.toPlainText()
                filterData.append(data)

        else:
            data = self.editTabsView.currentWidget().toPlainText()
            filterData.append(data)
        Fiter().filter(searchTag, filterData).pipe(
            ops.subscribe_on(scheduler.ThreadPoolScheduler()),
            qtScheduler.QtScheduler()
        ).subscribe(
            on_next=lambda filterResult: self.handlerFilterResult(filterResult),
            on_error=lambda e: self.handlerFilterErrorResult(e),
        )

    def handlerFilterErrorResult(self, error):
        print("error")
        print(error)
        box = QErrorMessage(self)
        box.showMessage(error, "结果提示")
        box.exec_()

    def handlerFilterResult(self, filterResult):
        self.editTabsView.currentWidget().handlerFilterResult(filterResult)

    def _initData(self):
        pass

    def tabCloseRequested(self, index):
        self.editTabsView.removeTab(index)

    def _initMenus(self):
        pass

    def showContextMenu(self, pos):
        index = self.treeView.indexAt(pos)

    def dragEnterEvent(self, event: PySide2.QtGui.QDragEnterEvent):
        print("dragEnterEvent")
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: PySide2.QtGui.QDropEvent):
        print("dropEvent")

        data = event.mimeData()
        if data.hasUrls():
            urls = data.urls()
            if len(urls) <= 0:
                return
            files = list()
            for fileUrl in urls:
                print("fileUrl:%s" % fileUrl)
                if fileUrl.isLocalFile():
                    files.append(fileUrl.toLocalFile())
            self.addFile(files)

    def addFile(self, files):

        def _createObserver(subscription: rx.typing.Subscription, scheduler) -> rx.Observable:
                for file in files:
                    print("file:%s" % file)
                    with open(file, mode='r') as f:
                        content = f.readlines()
                    subscription.on_next(Class.LogInfo(file, "".join(content)))

        rx.create(_createObserver).pipe(
            ops.subscribe_on(scheduler.ThreadPoolScheduler()),
            qtScheduler.QtScheduler()
        ).subscribe(
            on_next=lambda value: self.handlerLogInfoResult(value)
        )




    def handlerLogInfoResult(self, data):
        RxBus.instance.post(data)

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent):
        print("LogFilterWidget close")
        RxBus.instance.unRegister(self)
        event.isAccepted()

    def handlerLogInfo(self, data: Class.LogInfo):
        print("handlerLogInfo %s" % data.title)
        editWidget = EditWidget()
        editWidget.setLogData(data)
        logTitle = data.title
        # (text, ok) = QInputDialog.getText(None, "日志名称", "名称", text=logTitle)
        # if ok and text:
        #     logTitle = text
        self.editTabsView.addTab(editWidget, data.title)
        # self.editTabsView.setTabWhatsThis(self.editTabsView.count() - 1, data.title)
        self.editTabsView.setTabToolTip(self.editTabsView.count() - 1, data.title)
        self.editTabsView.setCurrentIndex(self.editTabsView.count() - 1)
        # self.editTabsView.setCurrentIndex(0)
        pass
