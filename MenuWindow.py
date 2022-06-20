import os
import urllib.request
from tkinter import messagebox
import CountriesWindow
import GameWindow
import tkinter as tk
from tkinter import *
import StartWindow
from tkinter.font import Font

#klasa umożliwiająca wybór trybu gry
class MenuWindow(tk.Frame):

    def __init__(self, master: tk):
        super().__init__(master)
        self.__defaultFont = Font(family='Courier New bold')
        self.__parent = master
        self.__menuFrame = tk.Frame(master)
        self.__optionsToolBar = tk.Frame(self.__parent)
        self.__menuFrame.pack(fill='both', expand=1)
        self.__menuFrame.config(background='#253439')
        self.__modeOption = None
        self.__optionsImages = []

        self.createView()
        self.toolBarOptions()

    def createView(self):
        startButton = tk.Button(self.__menuFrame, text="Back", font=(self.__defaultFont, 20), foreground='#253439',
                                borderwidth=0, command=self.toTheMenu)
        startButton.pack(side=LEFT, anchor=NW, padx=(10, 1), pady=10)

        labelMode = tk.Label(self.__menuFrame, text='Choose game mode', font=('Algerian', 50), background='#253439',
                             foreground='white')
        labelMode.pack(side=LEFT, anchor=N, pady=150, padx=330)

    #tworzenie paska wyboru trybu gry
    def toolBarOptions(self):
        self.__optionsToolBar.config(background='white')

        for image, command in (
                ("images/fast.png", self.chooseCountryFast),
                ("images/great.png", self.chooseCountryGreat),
                ("images/learn.png", self.learnMode),
                ("images/quiz.png", self.chooseQuizMode)):
            image = os.path.join(os.path.dirname(__file__), image)
            try:
                image = tk.PhotoImage(file=image)
                self.__optionsImages.append(image)
                button = tk.Button(self.__optionsToolBar, image=image,
                                   command=command, borderwidth=0)
                button.grid(row=0, column=len(self.__optionsImages) - 1)
            except tk.TclError as err:
                print(err)
        self.__optionsToolBar.pack()
        self.__optionsToolBar.rowconfigure(index=1, weight=1)
        self.__optionsToolBar.columnconfigure(index=1, weight=1)

    #ustawianie odpowiedniego trybu gry i przejście do kolejnego okna aplikacji
    def chooseQuizMode(self):
        self.__modeOption = 'quiz'
        self.toTheCountries()

    def chooseCountryFast(self):
        self.__modeOption = 'fast'
        self.toTheCountries()

    def chooseCountryGreat(self):
        self.__modeOption = 'great'
        self.toTheCountries()

    def toTheCountries(self):
        self.__menuFrame.destroy()
        self.__optionsToolBar.destroy()
        CountriesWindow.CountriesWindow(self.__parent, self.__modeOption)

    def learnMode(self):
        if not self.internetOn():
            messagebox.showinfo("No internet",
                                '''There is no internet connection, please try again later ...''')
        else:
            self.__modeOption = 'learn'
            self.__menuFrame.destroy()
            self.__optionsToolBar.destroy()
            GameWindow.GameWindowLearn(self.__parent)

    def toTheMenu(self):
        self.__menuFrame.destroy()
        self.__optionsToolBar.destroy()
        StartWindow.StartWindow(self.__parent)

    #sprawdzanie dostępu do internetu
    @staticmethod
    def internetOn():
        try:
            urllib.request.urlopen("http://www.kite.com", timeout=6)
            return True
        except:
            return False

