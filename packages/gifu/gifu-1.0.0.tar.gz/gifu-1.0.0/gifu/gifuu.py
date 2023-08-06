from tkinter import *
from tkinter import scrolledtext
#from tkinter.ttk import *

import tkinter as tk
from tkinter import ttk

from googletrans import Translator
translator = Translator()

from datetime import datetime


#from tkinter import filedialog
from tkinter import Menu

from tkinter import messagebox

class Janela:
    """docstring for Janela"""
    def __init__(self, master):
        self.bd = []
        self.listacaixa = []
        self.bd_anki = []

        self.janelas = master
        #janela = Tk()
        self.janelas.geometry("900x600+200+100")
        self.janelas.title("GIFU")
        #self.janelas.wm_iconbitmap("@gifu.xbm") 



        self.menu = tk.Menu(self.janelas)
        self.menu.add_command(label="Sobre", command=self.menuSobre)
        self.janelas.config(menu=self.menu)



        self.textoquadro = tk.Frame(self.janelas)
        self.barraprogressoquadro = tk.Frame(self.janelas)
        self.botaoquadro = tk.Frame(self.janelas)
        self.listaquadro = tk.Frame(self.janelas)

        self.textoquadro.pack(side='top', fill=tk.X)
        self.barraprogressoquadro.pack(side= tk.TOP, fill=tk.X)
        self.botaoquadro.pack(side= tk.LEFT)
        self.listaquadro.pack(side= tk.RIGHT, fill=tk.X, expand=True)


        self.texto = scrolledtext.ScrolledText(self.textoquadro,width=60,height=15)
        self.texto.pack(fill='x', expand=False )
        self.texto.insert(tk.INSERT, "Limpe esse texto, e cole o seu a traduzir")

        self.barraprogresso = ttk.Progressbar(self.barraprogressoquadro, length=200)
        self.barraprogresso.pack()

        self.bt=tk.Button(self.botaoquadro, text="Limpar", command=self.limpartextbox)
        self.bt.pack(side= tk.TOP, fill=tk.X, padx='10', pady='10')

        self.botaoo=tk.Button(self.botaoquadro, text="traduzir palavras", command=self.enviarpalavras)
        self.botaoo.pack(side= tk.TOP, fill=tk.X, padx='10', pady='10')

        self.botaooo=tk.Button(self.botaoquadro, text="mostrar palavras", command=self.cp_mylist)
        self.botaooo.pack(fill=tk.X, padx='10', pady='10')

        self.botaoooo=tk.Button(self.botaoquadro, text="criar anki", command=self.cardAnki)
        self.botaoooo.pack(fill=tk.X, padx='10', pady='10')

        self.botaoooo=tk.Button(self.botaoquadro, text="ver bdS", command=self.imprimirlis)
        self.botaoooo.pack(fill=tk.X, padx='10', pady='10')

        self.mensagem = tk.Label(self.barraprogressoquadro, text="GIFU", font="impact 30")
        self.mensagem.pack()

        self.scrollbar = tk.Scrollbar(self.listaquadro)
        self.scrollbar.pack( side = tk.RIGHT, fill=tk.Y )

        self.palavrastraduzidas = tk.Label(self.barraprogressoquadro, text=" ", font="impact 10")
        self.palavrastraduzidas.pack()

        self.minhalista = tk.Listbox(self.listaquadro, yscrollcommand = self.scrollbar.set, font="FreeSans 20")
        self.minhalista.pack( side = RIGHT, fill = X, expand=True )
        self.scrollbar.config( command = self.minhalista.yview )

    def imprimirminhalista(self):
            for linha in self.listacaixa:
                self.minhalista.insert(END, linha)    
    

    def adicionaraquivo(self):
        self.textoagora = self.texto.get(1.0, END)
        with open("tekisuto.txt", "w") as self.armazena:
           	self.armazena.write(self.textoagora)

    def adicionabd(self):
        self.abriarquivo = open("tekisuto.txt", "r")
        self.textoagoraa = self.abriarquivo.readlines()
        for line in self.textoagoraa:
        	# print(line)
        	line = line[:-1]  # retira a quebra de linha do texto.
        	self.bd.append(line.split(" "))
        	    #print(bd)
        self.abriarquivo.close()


    def lista_traduzidas(self, nometraduzi):
        self.palavrastraduzidas["text"] = "Aguarde"
        self.controlando = ' '
        self.controle_anki = ' '    #ajusta = 0
        self.tamanhodbarra = len(self.nometraduzi)
        self.valor = 0
        for x in self.nometraduzi:
            try:
                self.traduzi = translator.translate(x, dest='pt')
                self.traduzir = str(self.traduzi.text)
                self.controlando = " | " + x + ": " + self.traduzir + " |  "
                self.controle_anki = x + " " + self.traduzir
                self.listacaixa.append(self.controlando)
                self.bd_anki.append(self.controle_anki)
                self.valor += 1
                self.barraprogresso["value"] = self.valor
                self.barraprogresso["maximum"] = self.tamanhodbarra
                self.barraprogresso.update()
                if self.valor == self.tamanhodbarra:
                    self.transformav = str(self.tamanhodbarra)
                    self.palavrastraduzidas["text"] = "("+self.transformav+") Palavras traduzidas, aperte no botao mostrar palavras"
                    self.palavrastraduzidas["foreground"] = "red"
            except TypeError:
                self.controlando = " | " + x + ": " + "(As traduções variam)" + " |  "
                self.listacaixa.append(self.controlando)
                self.valor += 1
                self.barraprogresso["value"] = self.valor
                self.barraprogresso["maximum"] = self.tamanhodbarra
                self.barraprogresso.update()
                if self.valor == self.tamanhodbarra:
                    self.transformav = str(self.tamanhodbarra)
                    self.palavrastraduzidas["text"] = "("+self.transformav+") Palavras traduzidas, aperte no botao mostrar palavras"
                    self.palavrastraduzidas["foreground"] = "red"

    def adiciona_palavra(self, bd):
        self.nometraduzi = []  # cria lista para armazenar as palavras a serem traduzidas
        for self.x in self.bd:  # verifica cada linha da minha matriz
            for self.celula in self.x:  # olha cada celula da minha linha
                self.pal = str(self.celula)  # converte em string a minha celula
                self.palav = self.pal[0]  # pega a primeira letra da minha string e guarda numa variavel
                    #print("funcao a BD: " + pal[0])                  #olhando se deu certo
                self.pala = '@'  # cria uma variavel que vai ta no texto que vai indica a palavra a ser traduzida
                if self.palav == self.pala:  # compara
                    self.adiciona = self.pal[1:]  # agora vai excluir o caracter @ que ta na posição 0 e vai adiciona da 1 em diante
                    self.nometraduzi.append(self.adiciona)  # adiciona a minha lista
        self.lista_traduzidas(self.nometraduzi)
            #print("nometraduzi")
            #print(nometraduzi)


    def cp_mylista(self):
        self.imprimirminhalista()


    def limpartextbox(self):
        self.texto.delete(1.0,END)
        self.minhalista.delete( 0, END)
        self.bd.clear()
        self.listacaixa.clear()
        self.barraprogresso.stop()
        self.palavrastraduzidas["text"]= "Insira o texto"
            #texto["font"] = ("Consolas",10)

        #def aoClicar(mostra_texto):
            #mensagem["text"]= "palavras traduzidas:\n"+mostra_texto
        	

    def enviarpalavras(self):
        self.mostra_texto = self.texto.get(1.0, END)
        self.adicionaraquivo()
        self.adicionabd()
        self.adiciona_palavra(self.bd)

    def cp_mylist(self):
        self.cp_mylista()

    def imprimirlis(self):
        print("bd_anki")
        print(self.bd_anki)
        print("bd")	
        print(self.bd)
        print("listacaixa")
        print(self.listacaixa)

    def cardAnki(self):
        self.armazenadoanki = ''
        for self.pala_du in self.bd_anki:
        	self.armazenadoanki += self.pala_du + "\n"
        self.data_e_hora_atuais = datetime.now()
        self.data_e_hora_em_texto = self.data_e_hora_atuais.strftime("%d_%m_%Y %H:%M_%S")
        self.nuvemanki = open("bdAnki_"+self.data_e_hora_em_texto+".txt", "w")
        self.nuvemanki.write(self.armazenadoanki)
        #armazenadoanki.close()
        self.nuvemanki.close()

    def menuSobre(self):
        messagebox.showinfo('Sobre o Gifu','Desenvolvido por narutoolavo. narutoolavo@outlook.com')




def main():
	#programa
	janela = tk.Tk()
	#if __name__ == '__main__':
	Janela(janela)
	janela.mainloop()

