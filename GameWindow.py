import random
from tkinter import messagebox
from PIL import ImageTk
import tkintermapview
from googletrans import Translator
import MenuWindow
import tkinter as tk
from tkinter import *

from tkinter.font import Font
import FileReader

DEFAULT_FILE = 'files/capitals.txt'

#główna klasa odpowiadająca za przebieg gry
class GameWindow(tk.Frame):

    def __init__(self, master: tk, countries: [], mode):
        super().__init__(master)
        self.__defaultFont = Font(family='Courier New bold')
        self.__parent = master
        self.__gameFrame = tk.Frame(master)
        self.__gameFrame.pack(fill='both', expand=1)
        self.__gameFrame.config(background='white')
        self.__mode = mode
        self.__numberOfMoves = 0
        self.__data = countries
        self.__countriesData = []
        self.__correctedData = []
        self.__filePath = DEFAULT_FILE
        self.__correctAnswersCounter = 0
        self.__answersCounter = 0
        self.__questionLabel = Label(self.__gameFrame, text="QUESTION LABEL", font=self.__defaultFont,
                                     background='white', foreground='#435e67')
        self.__correctnessLabel = Label(self.__gameFrame, text='', font=self.__defaultFont, background='white',
                                        foreground='red', anchor=tk.W)
        self.__correctAnswer = Label(self.__gameFrame, text='', font=self.__defaultFont, background='white',
                                     foreground='#4DD0E1')
        self.__counterLabel = Label(self.__gameFrame, text=str(self.__answersCounter) + '/' + str(self.__numberOfMoves),
                                    font=self.__defaultFont, background='white', foreground='#F06292')
        self.__index = 0
        self.__translator = Translator()
        self.__mapWidget = tkintermapview.TkinterMapView(self.__gameFrame, width=1000, height=700, corner_radius=0,
                                                         max_zoom=6)
        self.__pauseImage = ImageTk.PhotoImage(file="images/pause2.png")
        self.__pauseLabel = Label(self.__gameFrame, image=self.__pauseImage)
        self.__pauseButton = tk.Button(self.__gameFrame, image=self.__pauseImage, command=self.choosingBox)
        self.__pauseButton.pack(side=TOP, anchor=W)

        self.__counterLabel.config(text=str(self.__answersCounter) + '/' + str(self.__numberOfMoves))
        self.readData()
        self.setNumberOfMoves()
        self.correctData()
        self.createView()
        self.playGame()

    #metoda definująca liczbę ruchów jakie ma użytkownik
    def setNumberOfMoves(self):
        if self.__mode == 'fast':
            if len(self.__countriesData) < 10:
                self.__numberOfMoves = len(self.__countriesData)
            else:
                self.__numberOfMoves = 10
        else:
            self.__numberOfMoves = len(self.__countriesData)

    #wczytywanie krajów z wybranych wcześniej kontynentów do tablicy
    def readData(self):
        fileReader = FileReader.FileReader(self.__filePath)
        for continent in self.__data:
            self.__countriesData += fileReader.chooseTerritory(continent)

    #przygotowywanie krajów do gry, tworzenie losowo ułożonej bazy pytań
    def correctData(self):
        checkSize = len(self.__countriesData)
        for i in range(checkSize):
            choice = random.choice(self.__countriesData)
            index = self.__countriesData.index(choice)
            del self.__countriesData[index]
            self.__correctedData.append(choice)

    #rozpoczęcie gry
    def playGame(self):
        self.click()
        self.__questionLabel.config(text="Which country's capital is " +
                                         str(self.__correctedData[self.__index][1]) + ' ?')

    #metoda umożliwiająca dodanie markera na mapę
    def click(self):
        self.__mapWidget.add_right_click_menu_command(label="Add Marker", command=self.add_marker_event,
                                                      pass_coords=True)

    #metoda wywoływana przez dodawanie markera do mapy
    def add_marker_event(self, coords):
        #opakowanie try except, aby użytkownik nie miał możliwości zaznaczenia zbiornika wodnego
        try:
            #czytanie współrzędnych zaznaczonych przez użytkownika i konwersja ich na nazwę państwa
            place = tkintermapview.convert_coordinates_to_country(coords[0], coords[1])
            #tłumaczenie nazwy państwa na język angielski
            translated = self.__translator.translate(place, dest='en')

            self.__answersCounter += 1
            self.__counterLabel.config(text=str(self.__answersCounter) + '/' + str(self.__numberOfMoves))
            if self.__answersCounter == self.__numberOfMoves:
                self.showResults()
            else:
                #sprawdzanie poprwaności odpowiedzi użytkownika z rzeczywistą odpowiedzią
                if self.checkCorrectness(translated.text):
                    self.__correctnessLabel.config(text='Correct!', foreground='#4DD0E1')
                    new_marker = self.__mapWidget.set_marker(coords[0], coords[1],
                                                             text=self.__correctedData[self.__index][0])
                else:
                    self.__correctnessLabel.config(text='Wrong! Correct is ' +
                                                        str(self.__correctedData[self.__index][0]).upper(),
                                                   foreground='#E91E63')
                    new_marker = self.__mapWidget.set_marker(coords[0], coords[1], text=translated.text)
                self.__index += 1
                self.__questionLabel.config(text="Which country's capital is " +
                                                 str(self.__correctedData[self.__index][1]) + ' ?')
        except:
            print("Wrong localization, it's not the country ...")
            self.__correctnessLabel.config(text='You need to choose territory ...', foreground='orange')

    #metoda sprawdzająca poprawność odpowiedzi użytkownika
    def checkCorrectness(self, place):
        if str(place) == str(self.__correctedData[self.__index][0]) or \
                (str(place) == str(self.__correctedData[self.__index][2])):
            self.__correctAnswersCounter += 1
            return True
        else:
            return False

    def showResults(self, event=None):
        reply = messagebox.showinfo(
            "Results",
            "This is your result: " + str(self.__correctAnswersCounter) + '/' + str(self.__numberOfMoves) +
            "\nDo you want to quit?",
            parent=self.__parent)
        event = event

        if reply:
            self.__gameFrame.destroy()
            MenuWindow.MenuWindow(self.__parent)

    def createView(self):
        self.__questionLabel.pack(side=TOP, anchor=N)
        self.__correctnessLabel.pack(side=TOP)
        self.__counterLabel.config(text=str(self.__answersCounter) + '/' + str(self.__numberOfMoves))
        self.__counterLabel.pack(side=TOP)
        self.__mapWidget.set_tile_server(
                "https://api.maptiler.com/maps/streets/256/{z}/{x}/{y}.png?key=g7FOdO6FbvTIQJsuxZpL", max_zoom=5)
        self.__mapWidget.pack(fill="both", expand=True)
        self.__mapWidget.set_zoom(0, False)
        self.__mapWidget.check_map_border_crossing()

    def choosingBox(self, event=None):
        reply = messagebox.askyesno(
            "PAUSE",
            "Are you sure, you want to quit?",
            parent=self.__parent)
        event = event
        if reply:
            self.__mode = ""
            self.__gameFrame.destroy()
            MenuWindow.MenuWindow(self.__parent)

#klasa odpowiadająca za tryb learn, tworzymy w niej widok z odpowiednią mapą i przycik umożliwiający nam powrót
class GameWindowLearn(tk.Frame):

    def __init__(self, master: tk):
        super().__init__(master)
        self.__defaultFont = Font(family='Courier New bold')
        self.__parent = master
        self.__gameFrame1 = tk.Frame(master)
        self.__gameFrame1.pack(fill='both', expand=1)
        self.__gameFrame1.config(background='white')
        self.__mapWidget = tkintermapview.TkinterMapView(self.__gameFrame1, width=1000, height=700, corner_radius=0,
                                                         max_zoom=6)
        self.__mapWidget.set_tile_server(
                        "https://api.maptiler.com/maps/openstreetmap/256/{z}/{x}/{y}.jpg?key=g7FOdO6FbvTIQJsuxZpL")
        self.__gameFrame1.config(background='white')

        self.__pauseImage = ImageTk.PhotoImage(file="images/pause2.png")
        self.__pauseLabel = Label(self.__gameFrame1, image=self.__pauseImage)
        self.__pauseButton = tk.Button(self.__gameFrame1, image=self.__pauseImage, command=self.choosingBox)
        self.__pauseButton.pack(side=TOP, anchor=W)
        self.__mapWidget.pack(fill="both", expand=True)
        self.__mapWidget.set_zoom(0, False)
        self.__mapWidget.check_map_border_crossing()

    def choosingBox(self, event=None):
        reply = messagebox.askyesno(
            "PAUSE",
            "Are you sure, you want to quit?",
            parent=self.__parent)
        event = event
        if reply:
            self.__gameFrame1.destroy()
            MenuWindow.MenuWindow(self.__parent)







