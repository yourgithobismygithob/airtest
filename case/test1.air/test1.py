# -*- encoding=utf8 -*-
__author__ = "luodan"

from airtest.core.api import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from airtest_selenium.proxy import WebChrome
driver = WebChrome()
driver.implicitly_wait(20)


auto_setup(__file__)
driver.get("chrome://welcome/")
driver.get("http://www.baidu.com")


