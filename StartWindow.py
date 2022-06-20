import tkinter
from tkinter import messagebox
from tkinter.font import Font
from tkinter import *
from PIL import ImageTk, Image
import LoginWindow
import RegisterWindow
import tkinter as tk

#klasa wyświetlająca się po uruchomieniu programu składa się głównie z elementów gui, tworzy menu
class StartWindow(tk.Frame):

    def __init__(self, master: Tk):
        super().__init__(master)
        self.__parent = master
        self.__parent.geometry('1500x750')
        self.__parent.title("GeoQuiz")
        self.__parent.rowconfigure(index=0, weight=999)
        self.__parent.columnconfigure(index=0, weight=999)
        self.__parent.configure(background='white')
        self.__parent.resizable(False, False)

        self.__frame = tkinter.Frame(self.__parent)
        self.__frame.config(background='#253439')
        self.__frame.pack(fill='both', expand=1)
        self.__defaultFont = Font(family='Courier New bold')
        background = Image.open("images/start.png")
        self.__backgroundPhoto = ImageTk.PhotoImage(background)
        self.__menu = tk.Menu(self.__parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.createView()
        self.createMenuBar()

    def createView(self):
        backgroundLabel = tk.Label(self.__frame, image=self.__backgroundPhoto)
        geoQuizLabel = Label(self.__frame, text="Welcome to GeoQuiz", font=('Algerian', 70),
                             background='#253439', foreground='white')
        geoQuizLabel.pack(side=TOP, anchor=N)

        siButton = tk.Button(self.__frame, text='Sign in', font=('Algerian', 30), background='white',
                             foreground='#253439', command=self.login, borderwidth=0)
        siButton.pack(side=LEFT,  anchor=N, pady=100, padx=(100,180))
        backgroundLabel.pack(side=LEFT, anchor=CENTER, padx=30)
        suButton = tk.Button(self.__frame, text='Sign up', font=('Algerian', 30), background='white',
                             foreground='#253439', command=self.register, borderwidth=0)
        suButton.pack(side=LEFT, anchor=N, pady=100, padx=(180, 100))

    def register(self):
        RegisterWindow.RegisterWindow(self.__parent)

    def login(self):
        LoginWindow.LoginWindow(self.__parent, self.__frame)

    def createMenuBar(self):
        self.__parent['menu'] = self.__menu
        fileMenu = tk.Menu(self.__menu)

        for label, command, shortcuttext, shortcut in (
                ("Quit", self.quitAction, "Ctrl+Q", "<Control-q>"),
                ("Help", self.instruction, "Ctrl+H", "<Control-h>")):
            if label is None:
                fileMenu.add_separator()
            else:
                fileMenu.add_command(label=label, underline=0, command=command, accelerator=shortcuttext)
                self.__parent.bind(shortcut, command)
        self.__menu.add_cascade(label="File", menu=fileMenu, underline=0)

        fileMenu = tk.Menu(self.__menu)
        for label, command, shortcut_text, shortcut in (
                ("Fast Game", self.fastInfo, "Ctrl+F", "<Control-f>"),
                ("Great Game", self.greatInfo, "Ctrl+G", "<Control-g>"),
                ("Learn Mode", self.learnInfo, "Ctrl+L", "<Control-l>"),
                ("Quiz Mode", self.flashInfo, "Ctrl+U", "<Control-u>")):
            fileMenu.add_command(label=label, underline=0,
                                 command=command, accelerator=shortcut_text)
            self.__parent.bind(shortcut, command)
        self.__menu.add_cascade(label="Info", menu=fileMenu, underline=0)

    def quitAction(self, event=None):
        reply = messagebox.askyesno(
            "Work finished",
            "Are you sure, you want to quit?",
            parent=self.__parent)
        event = event

        if reply:
            self.__parent.destroy()

    @staticmethod
    def instruction(event=None):
        messagebox.showinfo("Instruction",
                            '''After signing in choose territory, mode and learn capital's all over the world. 
                            \nIn fast and great mode click right mouse button to add marker to your map.''')

    @staticmethod
    def fastInfo(event=None):
        messagebox.showinfo("Fast Game",
                            '''Choose territory and answer 10 quick questions. 
                            \nClick right mouse button to add marker on your map and answer the quiestion.''')

    @staticmethod
    def greatInfo(event=None):
        messagebox.showinfo("Great Game",
                            '''Choose territory and guess all capital's from that territory. 
                            \nClick right mouse button to add marker on your map and answer the quiestion.''')

    @staticmethod
    def learnInfo(event=None):
        messagebox.showinfo("Learn Mode",
                            '''Watch map and learn countries and capitals. 
                            \nCapitals are those cities which have little black dot inside circle next to the name.''')

    @staticmethod
    def flashInfo(event=None):
        messagebox.showinfo("Quiz Mode",
                            '''Answer the question about the capitals and score points''')

