from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.common.exceptions import *
import random
from selenium.webdriver.common.keys import Keys
from Roleta import Roleta
import pyautogui
import pandas as pd
from datetime import datetime, timedelta
import time
from Telegram import Telegram


# auto-py-to-exe


class Main:
    def __init__(self):
        self.nav_blaze = webdriver.Chrome(ChromeDriverManager().install())
        self.nav_telegram = webdriver.Chrome(ChromeDriverManager().install())

        self.wait_blaze = WebDriverWait(
            self.nav_blaze,
            10,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException,
            ],
        )

        self.wait_telegram = WebDriverWait(
            self.nav_telegram,
            10,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException,
            ],
        )

    def start(self):

        self.nav_blaze.get("https://blaze.com/pt")
        self.nav_blaze.maximize_window()


        self.nav_telegram.get("https://web.telegram.org/k/")
        self.nav_telegram.maximize_window()

        pyautogui.alert(text='O Bot te da um tempo de 15 segundos para você fazer o login e deixar na conversa desejada', title='Faça o login',
                        button='OK')
        time.sleep(15)

        while pyautogui.confirm(text='Login ja foi feito?', title='Podemos continuar?',
                                buttons=['Sim', 'Não']) != "Sim":
            pyautogui.alert(text='O Bot te dará mais 10 segundos para você fazer o login', title='Faça o login',
                            button='OK')
            time.sleep(10)

        self.nav_telegram.set_window_size(500, 700)

        self.botao_crash = self.wait_blaze.until(
            CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div[3]/ul/li[1]/a')))
        self.botao_roleta = self.wait_blaze.until(
            CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div[3]/ul/li[2]/a')))
        self.botao_mine = self.wait_blaze.until(
            CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div[3]/ul/li[3]/a')))

        self.telegram = Telegram(self.nav_telegram, self.wait_telegram)
        self.startRoleta()


    def startRoleta(self):
        self.botao_roleta.click()
        estrategias = []

        while True:
            try:
                qtd_estrategias = int(pyautogui.prompt('Quantas estratégias serão inseridas?'))
                if qtd_estrategias > 0:
                    break
            except ValueError:
                print(ValueError)

        for x in range(qtd_estrategias):
            valido = False
            while not valido:
                try:
                    estrategia = pyautogui.prompt(
                        f'qual a {x + 1}° estrategia?\n"P" para preto, "V" para vermelho e "B" para branco \nresultados separados por ","').replace(
                        ".", ",").replace(";", ",").replace(" ", ",").replace("/", ",").lower()
                    est = estrategia.split(",")
                    if len(est) > 2:
                        valido = True

                    for item in est:
                        if item not in ["p", "b", "v"]:
                            valido = False

                    estrategias.append(estrategia)

                except ValueError:
                    print(ValueError)


        mensagem_aviso = pyautogui.prompt('mensagem de aviso \n("{cor}" será substituido pelo cor a ser jogada seguindo a estrategia)')
        mensagem_confirmcao = pyautogui.prompt('mensagem de confirmação de aposta \n("{cor}" será substituido pelo cor a ser jogada seguindo a estrategia)')
        mensagem_win = pyautogui.prompt('mensagem de win \n("{cor}" será substituido pelo cor resultado da roleta)')
        mensagem_loss = pyautogui.prompt('mensagem de loss \n("{cor}" será substituido pelo cor resultado da roleta)')

        roleta = Roleta(self.nav_blaze, self.wait_blaze, estrategias, mensagem_aviso, mensagem_confirmcao, mensagem_win, mensagem_loss, self.telegram)
        time.sleep(1)

        # botao_propaganda = self.wait_blaze.until(
        #     CondicaoExperada.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/i')))
        #
        # if botao_propaganda.is_displayed():
        #     botao_propaganda.click()
        #     time.sleep(1)

        ultimo_resultado = roleta.getUltimoResultadoRoleta()
        #print("Ultimo resultado")
        roleta.printUltimoResultado()

        while True:
            resultado_agora = roleta.getUltimoResultadoRoleta()
            if resultado_agora != ultimo_resultado:
                #print("saiu novo resultado")
                roleta.printUltimoResultado()
                ultimo_resultado = resultado_agora
                time.sleep(1)

            time.sleep(2)

    def error(self):
        print("Ocorreu um erro")
        self.nav_blaze.close()
        self.nav_telegram.close()




main = Main()
# main.start()

try:
    main.start()

except:
    main.error()
