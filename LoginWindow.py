from tkinter.font import Font
import MenuWindow
import User
import tkinter as tk
from tkinter import *

#klasa umożliwiająca logowanie użytkownika do systemu
class LoginWindow(tk.Frame):

    def __init__(self, master: tk, frame: Frame):
        super().__init__(master)
        self.__parent = master
        self.__frame = frame
        self.__loginWindow = Toplevel(self.__parent)
        self.__loginWindow.config(background='#253439')
        self.__loginWindow.geometry('500x650')
        self.__loginWindow.configure(background='#FADBD8')

        self.__informationLabel = None
        self.__status = None
        self.__defaultFont = Font(family='Courier New bold')

        self.__username = StringVar()
        self.__password = StringVar()
        self.createFields()

    def createFields(self):
        startButton = tk.Button(self.__loginWindow, text="Back", font=self.__defaultFont, foreground='#435e67',
                                borderwidth=0, command=self.toTheMenu)
        startButton.pack(anchor=NW, padx=10, pady=10)
        self.__informationLabel = tk.Label(self.__loginWindow, text='Login to become geo master!',
                                           background='#FADBD8', foreground='#435e67', font=(self.__defaultFont, 20))
        self.__informationLabel.pack(pady=(50, 10))

        userNameLabel = tk.Label(self.__loginWindow, text="Username", background='#FADBD8', foreground='#435e67',
                                 font=self.__defaultFont)
        userNameLabel.pack(pady=10)
        userNameEntry = Entry(self.__loginWindow, font=(self.__defaultFont, 15), textvariable=self.__username, width=15)
        userNameEntry.pack(pady=(10, 20))

        userPasswordLabel = tk.Label(self.__loginWindow, text="Password", background='#FADBD8', foreground='#435e67',
                                     font=self.__defaultFont)
        userPasswordLabel.pack(pady=10)
        userPasswordEntry = Entry(self.__loginWindow, font=(self.__defaultFont, 15), textvariable=self.__password,
                                  width=15, show='*')
        userPasswordEntry.pack(pady=(10, 20))
        loginButton = tk.Button(self.__loginWindow, text='Sign in', width=15, font=self.__defaultFont,
                                background='#435e67', foreground='white', borderwidth=0, command=self.login)
        loginButton.pack(pady=50)
        self.__status = tk.Label(self.__loginWindow, text="", font=('arial', 15), background='#FADBD8',
                                 foreground='#435e67')
        self.__status.pack()

    #przejście do menu głównego gry
    def getToMenuGame(self):
        self.__loginWindow.destroy()
        MenuWindow.MenuWindow(self.__parent)
        self.__frame.destroy()

    #wczytanie wartości pól wpisanych przez użytkownika i sprawdzanie ich poprawności
    def login(self):
        if self.__username.get == "" or self.__password.get() == "":
            self.__status.config(text="Please complete the required field!", fg="orange")
        else:
            user = User.User()
            raport = User.User.login(user, self.__username, self.__password)
            if raport:
                self.getToMenuGame()
            else:
                self.__status.config(text="Invalid password or username")

    #powrót do ekranu głównego
    def toTheMenu(self):
        self.__loginWindow.destroy()
