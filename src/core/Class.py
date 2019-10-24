#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FilterResult:
    def __init__(self, tag: str = "", value: str = "", orgTag: str = ""):
        self.orgTag = orgTag
        self.tag = tag
        self.value = value
