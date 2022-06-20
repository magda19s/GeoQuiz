import os
from tkinter import messagebox
import QuizWindow
import GameWindow
import MenuWindow
import urllib.request
import tkinter as tk
from tkinter import *
from tkinter.font import Font

#klasa umożliwiająca wybór terytorium (kontynentu) biorącego udział w grze
class CountriesWindow(tk.Frame):

    def __init__(self, master: tk, mode):
        super().__init__(master)
        self.__parent = master
        self.__countriesFrame = tk.Frame(master)
        self.__continentsToolBar = tk.Frame(self.__parent)
        self.__countriesFrame.pack(fill='both', expand=1)
        self.__countriesFrame.config(background='white')
        self.__defaultFont = Font(family='Courier New bold')
        self.__warningLabel = tk.Label(self.__countriesFrame, text='You need to choose territory',
                                       font=self.__defaultFont, background='white', foreground='red')
        self.__mode = mode
        self.__usersChoice = []
        self.__continentsImages = []
        self.__ifClicked = []
        self.__choiceLabel6 = None
        self.__choiceLabel5 = None
        self.__choiceLabel4 = None
        self.__choiceLabel3 = None
        self.__choiceLabel2 = None
        self.__choiceLabel1 = None
        self.__menuFrame = None
        self.createBoard()

    def createBoard(self):
        startButton = tk.Button(self.__countriesFrame, text="Back", font=(self.__defaultFont, 20),
                                foreground='#435e67', borderwidth=0, command=self.toTheMode)
        startButton.pack(anchor=NW, padx=10, pady=10)
        infoLabel = tk.Label(self.__countriesFrame, text='CHOOSE TERRITORY', font=self.__defaultFont,
                             background='white', foreground='#435e67')
        infoLabel.pack(anchor=N)
        playButton = tk.Button(self.__countriesFrame, text='PLAY', width=10, font=(self.__defaultFont, 20),
                               background='#435e67', foreground='white', command=self.playGame)
        playButton.pack(side=BOTTOM, pady=10)

        self.__continentsToolBar.config(background='white')

        for image, command, clicked in (
                ("images/afryka.png", self.addAfrica, False),
                ("images/azja.png", self.addAsia, False),
                ("images/europa.png", self.addEurope, False),
                ("images/amerykapolnocna.png", self.addAmericaNorth, False),
                ("images/amerykapoludniowa.png", self.addAmericaSouth, False),
                ("images/australia.png", self.addAustralia, False)):
            image = os.path.join(os.path.dirname(__file__), image)
            try:
                image = tk.PhotoImage(file=image)
                self.__continentsImages.append(image)
                self.__ifClicked.append(clicked)
                button = tk.Button(self.__continentsToolBar, image=image,
                                   command=command)
                button.grid(row=0, column=len(self.__continentsImages) - 1)
            except tk.TclError as err:
                print(err)
        self.__continentsToolBar.pack()
        self.__continentsToolBar.rowconfigure(index=1, weight=1)
        self.__continentsToolBar.columnconfigure(index=1, weight=1)

    def toTheMode(self):
        self.__countriesFrame.destroy()
        self.__continentsToolBar.destroy()
        MenuWindow.MenuWindow(self.__parent)

    #rozpoczęcie gry w zależności od trybu
    def playGame(self):
        if not self.__usersChoice:
            self.__warningLabel.pack(anchor=CENTER, pady=10)
        else:
            if self.__mode == 'quiz':
                self.__countriesFrame.destroy()
                self.__continentsToolBar.destroy()
                QuizWindow.QuizWindow(self.__parent, self.__usersChoice)
            else:
                if not self.internetOn():
                    messagebox.showinfo("No internet",
                                        '''There is no internet connection, please try again later ...''')
                else:
                    self.__countriesFrame.destroy()
                    self.__continentsToolBar.destroy()
                    GameWindow.GameWindow(self.__parent, self.__usersChoice, self.__mode)

    #metody dodające wybrany przez użytkownika kontynent
    def addAfrica(self):
        if 'Africa' in self.__usersChoice and self.__ifClicked[0]:
            self.__choiceLabel1.destroy()
            index = self.__usersChoice.index('Africa')
            del self.__usersChoice[index]
            self.__ifClicked[0] = False

        else:
            self.__warningLabel.destroy()
            self.__warningLabel = tk.Label(self.__countriesFrame, text='You need to choose territory',
                                           font=self.__defaultFont, background='white', foreground='red')
            self.__usersChoice.append('Africa')
            self.__choiceLabel1 = tk.Label(self.__countriesFrame, text='Africa', font=self.__defaultFont,
                                           background='white', foreground='#435e67')
            self.__choiceLabel1.pack(anchor=CENTER, pady=5)
            self.__ifClicked[0] = True

    def addEurope(self):
        if 'Europe' in self.__usersChoice and self.__ifClicked[2]:
            self.__choiceLabel2.destroy()
            index = self.__usersChoice.index('Europe')
            del self.__usersChoice[index]
            self.__ifClicked[2] = False

        else:
            self.__warningLabel.destroy()
            self.__warningLabel = tk.Label(self.__countriesFrame, text='You need to choose territory',
                                           font=self.__defaultFont, background='white', foreground='red')
            self.__usersChoice.append('Europe')
            self.__choiceLabel2 = tk.Label(self.__countriesFrame, text='Europe', font=self.__defaultFont,
                                           background='white', foreground='#435e67')
            self.__choiceLabel2.pack(anchor=CENTER, pady=5)
            self.__ifClicked[2] = True

    def addAustralia(self):
        if 'Australia and Oceania' in self.__usersChoice and self.__ifClicked[5]:
            self.__choiceLabel3.destroy()
            index = self.__usersChoice.index('Australia and Oceania')
            del self.__usersChoice[index]
            self.__ifClicked[5] = False
        else:
            self.__warningLabel.destroy()
            self.__warningLabel = tk.Label(self.__countriesFrame, text='You need to choose territory',
                                           font=self.__defaultFont, background='white', foreground='red')
            self.__usersChoice.append('Australia and Oceania')
            self.__choiceLabel3 = tk.Label(self.__countriesFrame, text='Australia and Oceania', font=self.__defaultFont,
                                           background='white', foreground='#435e67')
            self.__choiceLabel3.pack(anchor=CENTER, pady=5)
            self.__ifClicked[5] = True

    def addAsia(self):
        if 'Asia' in self.__usersChoice and self.__ifClicked[1]:
            self.__choiceLabel4.destroy()
            index = self.__usersChoice.index('Asia')
            del self.__usersChoice[index]
            self.__ifClicked[1] = False

        else:
            self.__warningLabel.destroy()
            self.__warningLabel = tk.Label(self.__countriesFrame, text='You need to choose territory',
                                           font=self.__defaultFont, background='white', foreground='red')
            self.__usersChoice.append('Asia')
            self.__choiceLabel4 = tk.Label(self.__countriesFrame, text='Asia', font=self.__defaultFont,
                                           background='white', foreground='#435e67')
            self.__choiceLabel4.pack(anchor=CENTER, pady=5)
            self.__ifClicked[1] = True

    def addAmericaNorth(self):
        if 'North America' in self.__usersChoice and self.__ifClicked[3]:
            self.__choiceLabel5.destroy()
            index = self.__usersChoice.index('North America')
            del self.__usersChoice[index]
            self.__ifClicked[3] = False

        else:
            self.__warningLabel.destroy()
            self.__warningLabel = tk.Label(self.__countriesFrame, text='You need to choose territory',
                                           font=self.__defaultFont, background='white', foreground='red')
            self.__usersChoice.append('North America')
            self.__choiceLabel5 = tk.Label(self.__countriesFrame, text='North America', font=self.__defaultFont,
                                           background='white', foreground='#435e67')
            self.__choiceLabel5.pack(anchor=CENTER, pady=5)
            self.__ifClicked[3] = True

    def addAmericaSouth(self):
        if 'South America' in self.__usersChoice and self.__ifClicked[4]:
            self.__choiceLabel6.destroy()
            index = self.__usersChoice.index('South America')
            del self.__usersChoice[index]
            self.__ifClicked[4] = False

        else:
            self.__warningLabel.destroy()
            self.__warningLabel = tk.Label(self.__countriesFrame, text='You need to choose territory',
                                           font=self.__defaultFont, background='white', foreground='red')
            self.__usersChoice.append('South America')
            self.__choiceLabel6 = tk.Label(self.__countriesFrame, text='South America', font=self.__defaultFont,
                                           background='white', foreground='#435e67')
            self.__choiceLabel6.pack(anchor=CENTER, pady=5)
            self.__ifClicked[4] = True

    #sprawdzenie dostępności do internetu
    @staticmethod
    def internetOn():
        try:
            urllib.request.urlopen("http://www.kite.com", timeout=6)
            return True
        except:
            return False
