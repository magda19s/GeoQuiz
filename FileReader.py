#klasa zajmująca się bazą pytań, wczytuje dane z pliku do słownika, a następnie wybiera z niego terytorium wskazane przez użytkownika
class FileReader:

    def __init__(self, path):
        self.__filePath = path
        self.__continents = ['Africa', 'South America', 'Asia', 'North America', 'Europe', 'Australia and Oceania']
        self.__allCountries = dict()
        for continent in self.__continents:
            self.__allCountries[continent] = []
        self.__countriesInGame = []
        self.readFile()

    #odczytywanie zawartości pliku
    def readFile(self):
        try:
            with open(self.__filePath, 'r', encoding="utf-8") as file:
                changedContinent = False
                temporaryContinent = self.__continents[4]
                for line in file:
                    for continent in self.__continents:
                        if continent == str(line).rstrip('\n'):
                            temporaryContinent = continent
                            changedContinent = True
                    if not changedContinent:
                        value = line.split(',')
                        value[0] = value[0].rstrip('\n')
                        value[0] = value[0].rstrip('\t')
                        value[1] = value[1].rstrip('\n')
                        value[1] = value[1].rstrip('\t')
                        value[2] = value[2].rstrip('\n')
                        self.__allCountries[temporaryContinent].append((value[0], value[1], value[2]))

                    else:
                        changedContinent = False

        except (FileNotFoundError, IOError):
            print("Wrong file or file path")
        except:
            print('Check the file, something went wrong .. ')

    #pobieranie państw ze wskazanego kontynentu (territory)
    def getTerritoryData(self, territory):
        if territory not in self.__allCountries.keys():
            print("There is no such territory")
            return []
        else:
            return self.__allCountries[territory]

    #wczytywanie państw do gry
    def chooseTerritory(self, *args):
        self.__countriesInGame = []
        for arg in args:
            values = self.getTerritoryData(arg)
            for value in values:
                self.__countriesInGame.append(value)
        return self.__countriesInGame



