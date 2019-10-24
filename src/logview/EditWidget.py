#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QTabWidget
from rxbus.core import RxBus
from src.BusData import Class

from .LogHighlighter import LogQSyntaxHighlighter


class EditWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.logData: Class.LogInfo = None
        self.resultMap = dict()
        self._initUI()
        self._initData()

    def getLogData(self):
        return self.logData

    def setLogData(self, data: Class.LogInfo):
        self.logData = data
        self.topText.setPlainText(self.logData.data)

    def toPlainText(self):
        return self.topText.toPlainText()

    def _initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.topText = QPlainTextEdit(self)
        self.topText.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.topText.setCenterOnScroll(True)
        self.topText.setAcceptDrops(False)
        self.topText.verticalScrollBar()
        self.bottomText = QTabWidget(self)
        self.bottomText.setDocumentMode(True)
        self.bottomText.setMovable(True)
        self.bottomText.setTabsClosable(True)
        self.bottomText.tabCloseRequested.connect(self.tabCloseRequested)
        self.mainLayout.addWidget(self.topText, 1)
        self.mainLayout.addWidget(self.bottomText, 1)
        self.setLayout(self.mainLayout)

    def tabCloseRequested(self, index):
        self.bottomText.removeTab(index)

    def _initData(self):
        pass

    #     self.topText.setPlainText('''10-18 16:52:37.542544 13034 13073 D _V_CommonModel: [VivoVideo]onLoaded
    # 10-18 16:52:37.545425 13034 13034 D EventBus: No subscribers registered for event class com.vivo.video.baselibrary.lifecycle.PlayerStateChangeEvent
    # 10-18 16:52:37.545536 13034 13034 D EventBus: No subscribers registered for event class org.greenrobot.eventbus.g
    # 10-18 16:52:37.559381  2359  2359 I _V_MainThreadMonitor: scheduleCheck true, true, 900
    # 10-18 16:52:37.561130 13034 13034 D _V_LiveTabFragment: [VivoVideo]liveCategory load onsuccess
    # 10-18 16:52:37.561572   714   791 D BufferLayer: triger signalLayerUpdate
    # 10-18 16:52:37.561937 13034 13034 D _V_LiveCategoryFragmentAdapter: [VivoVideo]com.vivo.video.app.home.HomeActivity@489a20a
    # 10-18 16:52:37.565738 13034 13034 D _V_BaseFragment: [VivoVideo]init onCreateView
    # 10-18 16:52:37.576986 13034 13034 I RepluginBridge: getApi,clazz:interface com.unionyy.mobile.vivo.api.VV2YYInfoAction
    # 10-18 16:52:37.577233 13034 13034 I RepluginBridge: getApi,clazz:interface com.unionyy.mobile.vivo.api.VV2YYAuthAction
    # 10-18 16:52:37.577331 13034 13034 I RepluginBridge: getApi,clazz:interface com.unionyy.mobile.vivo.api.VV2YYInfoAction
    # 10-18 16:52:37.577359 13034 13034 I RepluginBridge: getApi,clazz:interface com.unionyy.mobile.vivo.api.VV2YYAuthAction''')

    def cursorPositionChanged(self):
        print("cursorPositionChanged")

    def handlerFilterResult(self, filterResult):
        result = self.resultMap.get(filterResult.orgTag)
        if result:
            print("已存在%s" % filterResult.orgTag)
            result.setPlainText(filterResult.value)
        else:
            print("未存在%s" % filterResult.orgTag)
            filterResultView = QPlainTextEdit(self)
            highlighter = LogQSyntaxHighlighter(filterResultView.document())
            highlighter.setHighlignterTags(filterResult.tag)
            filterResultView.setPlainText(filterResult.value)
            filterResultView.setLineWrapMode(QPlainTextEdit.NoWrap)
            filterResultView.cursorPositionChanged.connect(self.cursorPositionChanged)
            self.bottomText.addTab(filterResultView, filterResult.orgTag)
            self.bottomText.setCurrentIndex(self.bottomText.count() - 1)
            self.resultMap.setdefault(filterResult.orgTag, filterResultView)

    def destroy(self, destroyWindow: bool = ..., destroySubWindows: bool = ...):
        RxBus.instance.unRegister(self)
        super.destroy(destroyWindow, destroySubWindows)
        print("destroy")

    def create(self, arg__1: int = ..., initializeWindow: bool = ..., destroyOldWindow: bool = ...):
        super.create(arg__1, initializeWindow, destroyOldWindow)
        print("create")
