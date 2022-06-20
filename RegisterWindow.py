import User
import tkinter as tk
from tkinter import *
from tkinter.font import Font

#klasa umożliwiająca rejestracje uzytkownika
class RegisterWindow:

    def __init__(self, master: tk):

        self.__parent = master
        self.__regiScreen = Toplevel(self.__parent)
        self.__regiScreen.geometry('500x650')
        self.__regiScreen.configure(background='#FADBD8')

        self.__defaultFont = Font(family='Courier New bold')
        self.__status = None
        self.__username = StringVar()
        self.__password = StringVar()
        self.__name = StringVar()
        self.__surname = StringVar()
        self.registration()

    def toTheStart(self):
        self.__regiScreen.destroy()

    def registration(self):
        startButton = tk.Button(self.__regiScreen, text="Back", font=self.__defaultFont, foreground='#435e67',
                                borderwidth=0, command=self.toTheStart)
        startButton.pack(anchor=NW, padx=10, pady=10)
        userNameLabel = tk.Label(self.__regiScreen, text="Username", background='#FADBD8', foreground='#435e67',
                                 font=self.__defaultFont)
        userNameEntry = Entry(self.__regiScreen, font=(self.__defaultFont, 15), textvariable=self.__username, width=15)
        userPasswordLabel = tk.Label(self.__regiScreen, text="Password", background='#FADBD8',
                                     foreground='#435e67', font=self.__defaultFont)
        userPasswordEntry = Entry(self.__regiScreen, font=(self.__defaultFont, 15), textvariable=self.__password,
                                  width=15, show='*')
        nameLabel = tk.Label(self.__regiScreen, text="Name", background='#FADBD8', foreground='#435e67',
                             font=self.__defaultFont)
        nameEntry = Entry(self.__regiScreen, font=(self.__defaultFont, 15), textvariable=self.__name, width=15)

        surnameLabel = tk.Label(self.__regiScreen, text="Surname", background='#FADBD8', foreground='#435e67',
                                font=self.__defaultFont)
        surnameEntry = Entry(self.__regiScreen, font=(self.__defaultFont, 15), textvariable=self.__surname, width=15)

        registerButton = tk.Button(self.__regiScreen, text='Sign up', font=self.__defaultFont, width=15,
                                   command=self.register, borderwidth=0, background='#435e67', foreground='white')

        self.__status = tk.Label(self.__regiScreen, text="", font=('arial', 15), background='#FADBD8',
                                 foreground='#435e67')

        userNameLabel.pack(pady=10)
        userNameEntry.pack(pady=10)
        userPasswordLabel.pack(pady=10)
        userPasswordEntry.pack(pady=10)
        nameLabel.pack(pady=10)
        nameEntry.pack(pady=10)
        surnameLabel.pack(pady=10)
        surnameEntry.pack(pady=10)
        registerButton.pack(pady=30)
        self.__status.pack()

    #wczytanie wartości pól wpisanych przez użytkownika, zabezpieczenie systemu przed brakiem danych
    def register(self):
        if self.__username.get() == "" or self.__password.get() == "" or self.__name.get() == "" \
                or self.__surname.get() == "":
            self.__status.config(text="Please complete the required field!", fg="orange")
        else:
            passwordCorrectnessChecker = self.checkPasswordCorrectness(self.__password.get())
            if passwordCorrectnessChecker:
                user = User.User()
                report = User.User.register(user, self.__username, self.__password, self.__name, self.__surname)
                if report:
                    self.__status.config(text="Account has been succesfully created", fg="#85929E")
                    self.toTheStart()
                else:
                    self.__status.config(text="The username has been already taken", fg="#E74C3C")
            else:
                self.__status.config(text="Check your password 8 letters required,\n remember it has to contain small "
                                          "and big letter,\n number and at least one special sign: ! @ # $ % ?",
                                     fg="#E74C3C")

    #sprawdzenie prawidłowości hasła
    @staticmethod
    def checkPasswordCorrectness(password):
        password = str(password)
        upperLetter = False
        lowerLetter = False
        number = False
        specialSign = False
        signs = ['!', '@', '#', '$', '%', '?']
        if len(password) < 8:
            return False
        else:
            for letter in password:
                if letter.isupper():
                    upperLetter = True
                if letter.islower():
                    lowerLetter = True
                if letter.isnumeric():
                    number = True
                else:
                    for sign in signs:
                        if letter == sign:
                            specialSign = True
            if upperLetter and lowerLetter and number and specialSign:
                return True
            else:
                return False
