#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rx

from src.core import Class


class Fiter:
    def __init__(self):
        print("Fiter")

    def filter(self, tagStr, data) -> rx.Observable:
        _tagStr = tagStr
        _datas = data

        def _createObserver(observer: rx.typing.Observable, scheduler):
            if len(_tagStr) <= 0:
                observer.on_error("输入过滤关键词为空")
            else:
                tags = _tagStr.split("|")
                orgDataList = list()
                for _data in _datas:
                     orgDataList.extend(_data.split("\n"))
                result = ""
                for item in orgDataList:
                    findResult = False
                    for tag in tags:
                        if item.find(tag) >= 0:
                            findResult = True
                            break
                    if findResult:
                        result = result + item + "\n"
                if result == "":
                    observer.on_error("过滤结果为空")
                else:
                    observer.on_next(Class.FilterResult(tags, result, _tagStr))
                    observer.on_completed()

        return rx.create(_createObserver)
