# -*- coding: utf-8 -*-
import unittest, time, re
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.firefox.options import Options

def isotime():
    """
    """
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') 
    return now

class Test0x1TV(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('-headless')
        
        fp = webdriver.FirefoxProfile()
        fp.update_preferences()        

        # driver = Firefox(executable_path='geckodriver', firefox_options=options)
        self.driver = webdriver.Firefox(firefox_options=options, firefox_profile=fp)
        self.driver.implicitly_wait(30)
        self.base_url = "http://0x1.tv/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def log(self, msg):
        print isotime(), msg

    def test_random0x1tv(self):
        self.log("Starting test")
        driver = self.driver
        driver.get(self.base_url)
        for i in xrange(10):
            driver.get("http://0x1.tv/Special:Random")
            pass
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
