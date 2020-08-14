# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 22:08:22 2020

@author: Meet Hariya
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def searcher(name):
    driver = webdriver.Chrome("C:\\webdrivers\\chromedriver")
    driver.get("https://amazon.com/")
    driver.find_element_by_id("twotabsearchtextbox").send_keys(name+Keys.ENTER)
    get_url = driver.current_url
    return get_url
