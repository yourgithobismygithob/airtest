# -*- encoding=utf8 -*-
__author__ = "luodan"

from airtest.core.api import *

auto_setup(__file__)
text("123")
keyevent("1")
driver.assert_exist("", "xpath", "请填写测试点.")
