from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options


import os
class DataScrapper:
    def __init__(self) -> None:
        # SELENIUM
        self.__options = Options()
        # self.__options.headless = True
        self.__options.add_argument('--log-level=3')
        self.__options.add_argument('--headless')
        self.driver = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()), options=self.__options)
        self.driver.minimize_window()



    def quit(self):
        self.driver.quit()
