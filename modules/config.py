from string import ascii_letters, digits

import random
import time


#*****************************************************************************
# Lista de targets para BuscadorPersonas.py
# Funcion "main"

target_list = "targets.txt"

# Lista de datos obtenidos de los diferentes bots
# Función "graphGenerator"

emailsData_list = []
phonesData_list = []
wikipediaData_list = []
youtubeData_list = []
companiesData_list = []
DNIData_list = []

#*****************************************************************************
# Lista de politicos de espana investigados o condenados
# Archivo findData.py

politicosSpain_investigados = "data/Corruptos/list-spain-11-5-2019.txt"

#*****************************************************************************
# Black List
#Archivo BuscadorPersonas.py
#Archivo BuscadorNick

BL_parserPhone = ["facebook.com", "instagram.com", "youtube.com", "twitter.com", "linkedin.com", "pinterest.com"]

#*****************************************************************************
#Fact checking list
FC_list = ["newtral.com", "maldita.es", "rtve.es"]

#*****************************************************************************
#Fack checking words list

FC_words_list = ["estudio", "universidad", "informe", "fuente", "origen", "sentencia"]

#*****************************************************************************
#Corruption keywords

FC_corruption_keywords = ["corrupción", "investigado", "investigada", "imputado", "imputada", "malversación", "estafador", "estafadora", "prevaricación", "comisión", "comisiones"]

#*****************************************************************************
# Banner principal
GREEN, RESET = "\033[92m", "\033[0m"

char = lambda i: " ".join(random.sample(ascii_letters + digits, k=i)).upper()

def shuffle(line, name_length):

    for x in range(0, random.randint(1, 9)):
        print("\t{}".format(char(name_length)), end="\r")
        time.sleep(0.4)

    print("\t" + line)

def print_banner(name="Dante's Gates Minimal Version", version="01.06.02", author="Jorge Coronado (aka @JorgeWebsec)"):

    name_length = len(name) + 4  
    name = " ".join(name.upper())  
    name = "{} \033[1m{} \033[0m{}".format(char(2), name, char(2))

    print("\n")
    lines = [char(name_length), name, char(name_length)]
    [shuffle(line, name_length) for line in lines]
    print("\n\t{}".format(author))
    print("\t{}\n".format(version))

    print("""
      ____________________________________________________________________________________________________

      Discleimer: This application allows you to create intelligence through open sources. 
      You do not access information that is not public. The author is not responsible for its use.
      ____________________________________________________________________________________________________

      Description: Dante's Gates Minimal Version is an open application with a GNU license for OSINT with
      Spanish and international sources. Currently it is maintained by Jorge Coronado and there are other
      versions such as mobile and APIs for your applications.
      ----
      Important: the author of this software is not responsible for it's use. The App aims to help
      researchers in OSINT, not to do evil. For more information contact the author.

      """)