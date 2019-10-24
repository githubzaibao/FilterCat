#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide2.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PySide2.QtCore import Qt, QRegExp, QRegularExpression
from typing import List


class LogQSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.tags = list()
        self.colos = [Qt.darkGreen, Qt.darkMagenta, Qt.darkRed, Qt.darkBlue, Qt.darkCyan, Qt.darkYellow]
        self.tagColorMap = dict()

    def setHighlignterTags(self, tags: List):
        self.tagColorMap = dict()

        self.tags = tags
        self.pattern = ""
        for index, tag in enumerate(self.tags):
            if index > len(self.colos):
                self.tagColorMap.setdefault(tag, self.colos[len(self.colos) - 1])
            else:
                self.tagColorMap.setdefault(tag, self.colos[index])

            if index == 0:
                self.pattern = self.pattern + tag
            else:
                self.pattern = self.pattern + "|" + tag

            self.pattern = self.pattern + ""
        print(self.pattern)

    def highlightBlock(self, text):
        myClassFormat = QTextCharFormat()
        myClassFormat.setFontWeight(QFont.Bold)

        expression = QRegularExpression(self.pattern)
        i = expression.globalMatch(text)

        while i.hasNext():
            match = i.next()
            myClassFormat.setForeground(self.tagColorMap[match.capturedTexts()[0]])
            self.setFormat(match.capturedStart(), match.capturedLength(), myClassFormat)
