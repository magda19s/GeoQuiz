import sqlite3

#klasa wykorzystująca bazę danych, w celu zrealizowania logowania i rejestracji użytkownika
class User:

    def __init__(self):
        self.__conn = None
        self.__cursor = None

    #metoda łącząca nas z bazą danych
    def database(self):
        try:
            self.__conn = sqlite3.connect("players.db")
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute(
                "CREATE TABLE IF NOT EXISTS `play` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, "
                "password TEXT, firstname TEXT, lastname TEXT)")
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    #metoda rejestrująca użytkownika w systemie
    def register(self, username, password, name, surname):
        try:
            self.database()
            self.__cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (username.get(),))
            if self.__cursor.fetchone() is not None:
                return False
            else:
                self.__cursor.execute("INSERT INTO `member` (username, password, firstname, lastname)"
                                      " VALUES(?, ?, ?, ?)",
                               (str(username.get()), str(password.get()), str(name.get()), str(surname.get())))
                self.__conn.commit()
                username.set("")
                password.set("")
                name.set("")
                surname.set("")
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
            return False
        finally:
            if self.__conn:
                self.__cursor.close()
                self.__conn.close()
            return True

    #metoda logująca użytkownika do systemu
    def login(self, username, password):
        try:
            self.database()
            self.__cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?",
                            (username.get(), password.get()))

            if self.__cursor.fetchone() is not None:
                return True
            else:
                return False
        except:
            print('SQLite error while logging ...')



