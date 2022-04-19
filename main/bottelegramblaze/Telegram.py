from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as CondicaoExperada
import time
from datetime import datetime

class Telegram:
    def __init__(self, Driver, Await):
        self.nav = Driver
        self.wait = Await

    def enviarMensagem(self, texto):
        input = self.nav.find_element_by_xpath('//*[@id="column-center"]/div/div/div[4]/div/div[1]/div/div[8]/div[1]/div[1]')
        input.send_keys(texto)
        input.send_keys(Keys.ENTER)