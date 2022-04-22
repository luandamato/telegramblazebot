from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
import time
from datetime import datetime


class Telegram:
    def __init__(self, Driver, Await):
        self.nav = Driver
        self.wait = Await

    def enviarMensagem(self, texto):
        JS_ADD_TEXT_TO_INPUT = """
              var elm = arguments[0], txt = arguments[1];
              elm.innerHTML += txt;
              elm.dispatchEvent(new Event('change'));
              """

        elem = self.nav.find_element_by_xpath('//*[@id="column-center"]/div/div/div[4]/div/div[1]/div/div[8]/div[1]/div[1]')

        print(f"mensagem enviada: {texto}")
        self.nav.execute_script(JS_ADD_TEXT_TO_INPUT, elem, texto)
        elem.send_keys(" ")
        self.verificaPopUpLink()
        elem.send_keys(Keys.ENTER)

    def enviarMensagemComLinkOculto(self, texto, palavra, link):
        JS_ADD_TEXT_TO_INPUT = """
                      var elm = arguments[0], txt = arguments[1];
                      elm.innerHTML += txt;
                      elm.dispatchEvent(new Event('change'));
                      """

        elem = self.nav.find_element_by_xpath(
            '//*[@id="column-center"]/div/div/div[4]/div/div[1]/div/div[8]/div[1]/div[1]')

        print(f"mensagem com link enviada: {texto}")
        self.nav.execute_script(JS_ADD_TEXT_TO_INPUT, elem, texto)
        self.addLinkOculto(link, palavra)
        self.verificaPopUpLink()
        elem.send_keys(Keys.ENTER)


    def apagarUltimaMensagem(self):
        try:
            actionChains = ActionChains(self.nav)
            print('apagando mensagem')
            lista = self.nav.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[3]/div/div/section/div')
            mensagem = lista[-1]
            time.sleep(0.7)
            actionChains.context_click(mensagem).perform()
            time.sleep(0.7)
            btn_delete = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[6]/div[8]')))
            btn_delete.click()
            time.sleep(1)
            delete = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/button[1]')))
            delete.click()
            time.sleep(0.7)
        except:
            print("erro ao apagar mensagem")

    def responderUltimaMensagem(self, texto):
        try:
            actionChains = ActionChains(self.nav)
            lista = self.nav.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[3]/div/div/section/div')
            mensagem = lista[-1]
            time.sleep(0.7)
            actionChains.context_click(mensagem).perform()
            time.sleep(0.7)
            btn_reply = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[6]/div[2]/div')))
            btn_reply.click()
            time.sleep(0.7)

            #nao pode chamar EnviarMensagem por conta do verificaPopUpLink que clica no x da resposta
            JS_ADD_TEXT_TO_INPUT = """
                                  var elm = arguments[0], txt = arguments[1];
                                  elm.innerHTML += txt;
                                  elm.dispatchEvent(new Event('change'));
                                  """

            elem = self.nav.find_element_by_xpath(
                '//*[@id="column-center"]/div/div/div[4]/div/div[1]/div/div[8]/div[1]/div[1]')

            print(f"respondendo ultima mensagem com: {texto}")
            self.nav.execute_script(JS_ADD_TEXT_TO_INPUT, elem, texto)
            elem.send_keys(Keys.ENTER)
        except:
            print("erro ao responder mensagem")


    def verificaPopUpLink(self):
        time.sleep(1)
        botao_propaganda = self.nav.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[2]/div/div/div[4]/div/div[1]/div/div[2]/button[2]')
        if botao_propaganda.is_displayed():
            botao_propaganda.click()
            time.sleep(1)


    def addLinkOculto(self, link, palavra):
        elem = self.nav.find_element_by_xpath('//*[@id="column-center"]/div/div/div[4]/div/div[1]/div/div[8]/div[1]/div[1]')
        for _ in range(5):
            elem.send_keys(Keys.DOWN)

        for _ in range(len(palavra)):
            elem.send_keys(Keys.SHIFT, Keys.ARROW_LEFT)


        btn_add_link = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]/button[7]')))
        btn_add_link.click()
        time.sleep(0.5)
        input_link = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/input')))
        input_link.send_keys(link)
        time.sleep(0.5)
        btn_ok = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div/button')))
        btn_ok.click()
        time.sleep(0.5)

