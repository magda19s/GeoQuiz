import tkinter as tk
import random
from tkinter import messagebox
from tkinter.font import Font
from tkinter import *
import MenuWindow
import FileReader

DEFAULT_FILE = 'files/capitals.txt'

#klasa odpowiedzialna za quiz
class QuizWindow(tk.Frame):

    def __init__(self, master: tk, data):
        super().__init__(master)
        self.__defaultFont = Font(family='Courier New bold')
        self.__parent = master
        self.__flashFrame = tk.Frame(master)
        self.__flashFrame.pack(fill='both', expand=1)
        self.__flashFrame.config(background='#FADBD8')
        self.__filePath = DEFAULT_FILE
        self.__data = data
        self.__countriesData = []
        self.__countriesInGame = []
        self.__index = 0
        self.__correctAnswersCounter = 0

        self.__answerOptions = []
        self.__orderOptions = []
        self.__button4 = None
        self.__button3 = None
        self.__button2 = None
        self.__button1 = None
        self.__correctnessLabel = None
        self.__correctLabel = None
        self.__totalLabel = None
        self.__countryLabel = None

        self.readData()
        self.createView()
        self.createAnswers()
        self.configureButtons()

    def createView(self):
        startButton = tk.Button(self.__flashFrame, text="Back", font=(self.__defaultFont, 20),
                                foreground='white', background='#435e67', borderwidth=0, command=self.toTheMode)

        startButton.pack(anchor=NW, padx=10, pady=10)
        self.__countryLabel = tk.Label(self.__flashFrame, text='What is the capital of ' +
                                       str(self.__countriesInGame[0][0]) + ' ?', font=(self.__defaultFont, 40),
                                       foreground='#435e67', background='#FADBD8')

        self.__countryLabel.pack(side=TOP, pady=(80, 0), padx=10)
        self.__totalLabel = tk.Label(self.__flashFrame, text="TOTAL: " + str(self.__index) + '/' +
                                     str(len(self.__countriesInGame)), font=(self.__defaultFont, 20),
                                     foreground='#435e67', background='#FADBD8')
        self.__totalLabel.pack(pady=10)
        self.__correctLabel = tk.Label(self.__flashFrame, text="CORRECT: " + str(self.__correctAnswersCounter),
                                       font=(self.__defaultFont, 20), foreground='#E91E63', background='#FADBD8')
        self.__correctLabel.pack(pady=10)
        self.__correctnessLabel = tk.Label(self.__flashFrame, text='', font=(self.__defaultFont, 20),
                                           foreground='#435e67', background='#FADBD8')
        self.__correctnessLabel.pack(pady=10, padx=10)
        self.__button1 = Button(self.__flashFrame, text='first', width=20, font=(self.__defaultFont, 20),
                                background='#435e67', foreground='white', command=self.checkCorrectnessButton1)
        self.__button1.pack(side=LEFT, pady=100, padx=(30, 20))
        self.__button2 = Button(self.__flashFrame, text='sec', width=20, font=(self.__defaultFont, 20),
                                background='#435e67', foreground='white', command=self.checkCorrectnessButton2)
        self.__button2.pack(side=LEFT, pady=100, padx=20)
        self.__button3 = Button(self.__flashFrame, text='3', width=20, font=(self.__defaultFont, 20),
                                background='#435e67', foreground='white', command=self.checkCorrectnessButton3)
        self.__button3.pack(side=LEFT, pady=100, padx=20)
        self.__button4 = Button(self.__flashFrame, text='4', width=20, font=(self.__defaultFont, 20),
                                background='#435e67', foreground='white', command=self.checkCorrectnessButton4)
        self.__button4.pack(side=LEFT, pady=100, padx=20)

    def toTheMode(self,event=None):
        reply = messagebox.askyesno(
            "PAUSE",
            "Are you sure, you want to quit?",
            parent=self.__parent)
        event = event

        if reply:
            self.__flashFrame.destroy()
            MenuWindow.MenuWindow(self.__parent)

    #wczytywanie państw i stolic z pliku na podstawie kontynentów wybranych przez użytkownika
    def readData(self):
        fileReader = FileReader.FileReader(self.__filePath)
        for continent in self.__data:
            self.__countriesData += fileReader.chooseTerritory(continent)
        checkSize = len(self.__countriesData)
        for i in range(checkSize):
            choice = random.choice(self.__countriesData)
            index = self.__countriesData.index(choice)
            del self.__countriesData[index]
            self.__countriesInGame.append(choice)

    #metoda odpowiedzialna za przebieg rozgrywki
    def playGame(self):
        self.__index += 1
        if self.__index >= len(self.__countriesInGame):
            self.end()
        else:
            self.__countryLabel.config(text='What is the capital of ' + str(self.__countriesInGame[self.__index][0]) +
                                       ' ?')
            self.__totalLabel.config(text="TOTAL: " + str(self.__index) + '/' + str(len(self.__countriesInGame)))
            self.createAnswers()
            self.configureButtons()

    #metoda wybierająca losowa odpowiedzi w danej rundzie, prawidłowa odpowiedź zawsze jest dodawana do opcji
    #pozostałe trzy są losowane z bazy państw z kontynentów wybranych przez użytkownika
    def createAnswers(self):
        self.__answerOptions = []
        self.__answerOptions.append(self.__countriesInGame[self.__index][1])
        checker = 0
        while checker != 3:
            choice = random.choice(self.__countriesInGame)
            if choice[1] in self.__answerOptions:
                pass
            else:
                self.__answerOptions.append(choice[1])
                checker += 1

    #konfiguracja przycisków z odpowiedziami
    def configureButtons(self):
        self.__orderOptions = []
        self.__button1.config(text=str(self.chooseAnswerToButton()))
        self.__button2.config(text=str(self.chooseAnswerToButton()))
        self.__button3.config(text=str(self.chooseAnswerToButton()))
        self.__button4.config(text=str(self.chooseAnswerToButton()))

    #dopasowanie odpowiedzi do przycisku
    def chooseAnswerToButton(self):
        choice = random.choice(self.__answerOptions)
        index = self.__answerOptions.index(choice)
        del self.__answerOptions[index]
        self.__orderOptions.append(choice)
        return choice

    #sprawdzenie poprawności odpowiedzi użytkownika w zależności od klikniętego przycisku
    def checkCorrectnessButton1(self):
        if self.__orderOptions[0] == self.__countriesInGame[self.__index][1]:
            self.__correctAnswersCounter += 1
            self.__correctnessLabel.config(text='Well done!')
            self.__correctLabel.config(text="CORRECT: " + str(self.__correctAnswersCounter))

        else:
            self.__correctnessLabel.config(text='Wrong! Correct is ' +
                                                str(self.__countriesInGame[self.__index][1]).upper())
        self.playGame()

    def checkCorrectnessButton2(self):
        if self.__orderOptions[1] == self.__countriesInGame[self.__index][1]:
            self.__correctAnswersCounter += 1
            self.__correctnessLabel.config(text='Well done')
            self.__correctLabel.config(text="CORRECT: " + str(self.__correctAnswersCounter))

        else:
            self.__correctnessLabel.config(text='Wrong! Correct is ' +
                                                str(self.__countriesInGame[self.__index][1]).upper())
        self.playGame()

    def checkCorrectnessButton3(self):
        if self.__orderOptions[2] == self.__countriesInGame[self.__index][1]:
            self.__correctAnswersCounter += 1
            self.__correctnessLabel.config(text='Well done')
            self.__correctLabel.config(text="CORRECT: " + str(self.__correctAnswersCounter))

        else:
            self.__correctnessLabel.config(text='Wrong! Correct is ' +
                                                str(self.__countriesInGame[self.__index][1]).upper())
        self.playGame()

    def checkCorrectnessButton4(self):
        if self.__orderOptions[3] == self.__countriesInGame[self.__index][1]:
            self.__correctAnswersCounter += 1
            self.__correctnessLabel.config(text='Well done')
            self.__correctLabel.config(text="CORRECT: " + str(self.__correctAnswersCounter))

        else:
            self.__correctnessLabel.config(text='Wrong! Correct is ' +
                                                str(self.__countriesInGame[self.__index][1]).upper())
        self.playGame()

    #koniec quizy, wypisanie wyników i wyjście z quizu
    def end(self, event=None):
        reply = messagebox.showinfo(
            "Results",
            "This is your result: " + str(self.__correctAnswersCounter) + '/' + str(len(self.__countriesInGame)) +
            "\nDo you want to quit?",
            parent=self.__parent)
        event = event

        if reply:
            self.__flashFrame.destroy()
            MenuWindow.MenuWindow(self.__parent)



