from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as CondicaoExperada
import time
from datetime import datetime
from Telegram import Telegram

class Roleta:
    def __init__(self, Driver, Await, estrategias, mensagem_aviso, mensagem_confirmcao, mensagem_win, mensagem_loss, telegram):
        self.nav = Driver
        self.wait = Await
        self.estrategias = estrategias
        self.mensagem_aviso = mensagem_aviso
        self.mensagem_confirmcao = mensagem_confirmcao
        self.mensagem_win = mensagem_win
        self.mensagem_loss = mensagem_loss
        self.lista_resultados = []
        self.apostou = False
        self.telegram = telegram
        self.cor_aposta = ""
        self.count_perdas = 0


    def getUltimoResultadoRoleta(self):
        self.ultimo_resultado = self.nav.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div')
        self.cor_ultimo = self.ultimo_resultado.get_attribute('class').split(' ')[1]
        self.numero_ultimo = 0
        if (self.cor_ultimo != "white"):
            self.numero_ultimo = self.ultimo_resultado.find_element_by_xpath('div').get_attribute('innerHTML')
        return self.ultimo_resultado

    def printUltimoResultado(self):
        #self.getUltimoResultadoRoleta()
        self.getHoraResultado()
        # print(f"cor = {self.cor_ultimo}, numero = {self.numero_ultimo}, hora = {self.horario_ultimo}\n")
        if len(self.lista_resultados) > 10:
            self.lista_resultados.pop(0)

        self.lista_resultados.append(self.cor_ultimo.replace('red', 'v').replace('black', 'p').replace('white', 'b'))
        self.verificaSinal()

    def getNumero(self):
        return self.numero_ultimo

    def getCor(self):
        return self.cor_ultimo

    def getHoraResultado(self):
        time.sleep(1)
        botao_Resultado = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[1]')))
        botao_Resultado.click()
        lbl_horario = self.wait.until(CondicaoExperada.presence_of_element_located((By.XPATH, '//*[@id="roulette-game-history"]/div[1]/h2')))

        lbl = lbl_horario.get_attribute('innerHTML')
        arrHorario = lbl.split(' ')
        self.horario_ultimo = arrHorario[len(arrHorario) - 2]
        botao_fechar = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[3]/div/div[1]')))
        botao_fechar.click()

    def verificaAvisoPrevio(self, lista_resultados, lista_estrategia):
        lista_estrategia.pop(-1)
        lista_estrategia.pop(-1)
        if len(lista_resultados) > len(lista_estrategia):
            remover = len(lista_resultados) - len(lista_estrategia)
            for _ in range(remover):
                lista_resultados.pop(0)

        #print(f"comparando estrategia {lista_estrategia} com resultados {lista_resultados} para aviso previo")
        return lista_estrategia == lista_resultados

    def verificaAvisoAposta(self, lista_resultados, lista_estrategia):
        lista_estrategia.pop(-1)
        if len(lista_resultados) > len(lista_estrategia):
            remover = len(lista_resultados) - len(lista_estrategia)
            for _ in range(remover):
                lista_resultados.pop(0)

        #print(f"comparando estrategia {lista_estrategia} com resultados {lista_resultados} para apostar\n")
        return lista_estrategia == lista_resultados

    def verificaSinal(self):
        if self.apostou:
            if self.cor_ultimo.replace('red', 'v').replace('black', 'p').replace('white', 'b') == self.cor_aposta:
                frase = self.mensagem_win.replace("{cor}", self.cor_aposta.replace("p", "PRETO").replace("v", "VERMELHO").replace("b", "BRANCO"))
                self.telegram.enviarMensagem(frase)
                print(frase)
                self.apostou = False
            else:
                self.count_perdas += 1

            if self.count_perdas >= 3:
                frase = self.mensagem_loss.replace("{cor}", self.cor_aposta.replace("p", "PRETO").replace("v", "VERMELHO").replace("b", "BRANCO"))
                self.telegram.enviarMensagem(frase)
                print(frase)
                self.apostou = False

        for estrategia in self.estrategias:
            estrategia_lista = estrategia.split(",")
            if self.verificaAvisoPrevio(self.lista_resultados.copy(), estrategia_lista.copy()):
                frase = self.mensagem_aviso.replace("{cor}", estrategia_lista[-1].replace("p", "PRETO").replace("v", "VERMELHO").replace("b", "BRANCO"))
                print(frase)
                self.telegram.enviarMensagem(frase)
                break
            elif self.verificaAvisoAposta(self.lista_resultados.copy(), estrategia_lista.copy()):
                frase = self.mensagem_confirmcao.replace("{cor}", estrategia_lista[-1].replace("p", "PRETO").replace("v", "VERMELHO").replace("b", "BRANCO"))
                print(frase)
                self.telegram.enviarMensagem(frase)
                self.apostou = True
                self.cor_aposta = estrategia_lista[-1]
                break


