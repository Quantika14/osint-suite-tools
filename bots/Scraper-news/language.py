class Language():
    def __init__(self,lang = 'es'):
        self.__lang = lang

    def getPhrases(self):
        ''' Recoger las frases de un archivo, asi se puede tener diferentes idiomas'''
        with open(f'./archivos/phrases-{self.__lang.lower()}.txt') as file:
            return file.read().splitlines()