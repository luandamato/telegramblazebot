from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as CondicaoExperada
import time
from datetime import datetime
from Telegram import Telegram


class Roleta:
    def __init__(self, Driver, Await, estrategias, mensagem_aviso, mensagem_confirmcao, mensagem_win, mensagem_loss,
                 telegram):
        self.nav = Driver
        self.wait = Await
        self.horario_ultimo = ""
        self.estrategias = estrategias
        self.mensagem_aviso = mensagem_aviso
        self.mensagem_confirmcao = mensagem_confirmcao
        self.mensagem_win = mensagem_win
        self.mensagem_loss = mensagem_loss
        self.lista_resultados = []
        self.apostou = False
        self.enviou_alerta = False
        self.acao_atual = False
        self.telegram = telegram
        self.cor_aposta = ""
        self.count_perdas = 0
        self.link = ""
        print(estrategias)

    def getUltimoResultadoRoleta(self):
        self.ultimo_resultado = self.nav.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div')
        self.cor_ultimo = self.ultimo_resultado.get_attribute('class').split(' ')[1]
        self.numero_ultimo = 0
        if (self.cor_ultimo != "white"):
            self.numero_ultimo = self.ultimo_resultado.find_element_by_xpath('div').get_attribute('innerHTML')
        return self.ultimo_resultado

    def printUltimoResultado(self):
        if len(self.lista_resultados) > 10:
            self.lista_resultados.pop(0)

        self.lista_resultados.append(self.cor_ultimo.replace('red', 'v').replace('black', 'p').replace('white', 'b'))
        self.verificaSinal()

    def getNumero(self):
        return self.numero_ultimo

    def getCor(self):
        return self.cor_ultimo

    def limparHistorico(self):
        while len(self.lista_resultados) > 2:
            self.lista_resultados.pop(0)

    def verificaAvisoPrevio(self, lista_resultados, lista_estrategia):
        lista_estrategia.pop(-1)
        lista_estrategia.pop(-1)
        if len(lista_resultados) > len(lista_estrategia):
            remover = len(lista_resultados) - len(lista_estrategia)
            for _ in range(remover):
                lista_resultados.pop(0)

        # print(f"comparando estrategia {lista_estrategia} com resultados {lista_resultados} para aviso previo")
        return lista_estrategia == lista_resultados

    def verificaAvisoAposta(self, lista_resultados, lista_estrategia):
        lista_estrategia.pop(-1)
        if len(lista_resultados) > len(lista_estrategia):
            remover = len(lista_resultados) - len(lista_estrategia)
            for _ in range(remover):
                lista_resultados.pop(0)

        # print(f"comparando estrategia {lista_estrategia} com resultados {lista_resultados} para apostar\n")
        return lista_estrategia == lista_resultados

    def verificaSinal(self):
        self.acao_atual = False

        if self.enviou_alerta:
            self.enviou_alerta = False
            self.telegram.apagarUltimaMensagem()

        if self.apostou:
            if self.cor_ultimo.replace('red', 'v').replace('black', 'p') == self.cor_aposta or self.cor_ultimo == "white":
                frase = self.formatarMensagem(self.mensagem_win, self.cor_aposta)
                if self.cor_ultimo == "white":
                    frase = "GREEN BRANCO ⚪⚪⚪"
                self.telegram.responderUltimaMensagem(frase)
                # self.telegram.enviarMensagem(frase)
                self.apostou = False
                self.count_perdas = 0
                self.limparHistorico()
            else:
                self.count_perdas += 1

            if self.count_perdas >= 3:
                frase = self.formatarMensagem(self.mensagem_loss, self.cor_aposta)
                self.telegram.responderUltimaMensagem(frase)
                # self.telegram.enviarMensagem(frase)
                self.apostou = False
                self.count_perdas = 0
                self.limparHistorico()

        else:
            for estrategia in self.estrategias:
                estrategia_lista = estrategia.split(",")
                if self.verificaAvisoAposta(self.lista_resultados.copy(), estrategia_lista.copy()):
                    frase = self.formatarMensagem(self.mensagem_confirmcao, estrategia_lista[-1])
                    self.telegram.enviarMensagemTeste(texto=frase, palavra=frase.split(' ')[-1], link=self.link)
                    self.apostou = True
                    self.enviou_alerta = False
                    self.cor_aposta = estrategia_lista[-1]
                    self.acao_atual = True
                    break
                elif self.verificaAvisoPrevio(self.lista_resultados.copy(), estrategia_lista.copy()):
                    frase = self.formatarMensagem(self.mensagem_aviso, estrategia_lista[-1])
                    self.telegram.enviarMensagemTeste(texto=frase, palavra=frase.split(' ')[-1], link=self.link)
                    # self.telegram.enviarMensagem(frase)
                    self.enviou_alerta = True
                    self.acao_atual = True
                    break

        #se for apagar so se nao efetivar o sinal
        # if self.enviou_alerta and not self.acao_atual:
        #     self.enviou_alerta = False
        #     self.telegram.apagarUltimaMensagem()

    def formatarMensagem(self, texto, cor):
        perdas = f'{self.count_perdas}'.replace('0', "SG").replace('1', 'G1').replace('2', 'G2')
        frase = texto.replace("{cor}", cor.replace("p", "⚫").replace("v", "🔴").replace("b","⚪")).replace("{perdas}", perdas)

        self.link = ""
        palavras = frase.split(" ", 1)
        if ("{link" in palavras[0]):
            self.link = palavras[0].split(":", 1)[1][:-1]
            frase = frase.split(" ", 1)[1]

        return frase

