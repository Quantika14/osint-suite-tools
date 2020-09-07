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

banner = """
▓█████▄  ▄▄▄       ███▄    █ ▄▄▄█████▓▓█████   ██████      ▄████  ▄▄▄     ▄▄▄█████▓▓█████   ██████    
▒██▀ ██▌▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒▓█   ▀ ▒██    ▒     ██▒ ▀█▒▒████▄   ▓  ██▒ ▓▒▓█   ▀ ▒██    ▒    
░██   █▌▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▒███   ░ ▓██▄      ▒██░▄▄▄░▒██  ▀█▄ ▒ ▓██░ ▒░▒███   ░ ▓██▄      
░▓█▄   ▌░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▒▓█  ▄   ▒   ██▒   ░▓█  ██▓░██▄▄▄▄██░ ▓██▓ ░ ▒▓█  ▄   ▒   ██▒   
░▒████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ░▒████▒▒██████▒▒   ░▒▓███▀▒ ▓█   ▓██▒ ▒██▒ ░ ░▒████▒▒██████▒▒   
 ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░░ ▒░ ░▒ ▒▓▒ ▒ ░    ░▒   ▒  ▒▒   ▓▒█░ ▒ ░░   ░░ ▒░ ░▒ ▒▓▒ ▒ ░   
 ░ ▒  ▒   ▒   ▒▒ ░░ ░░   ░ ▒░    ░     ░ ░  ░░ ░▒  ░ ░     ░   ░   ▒   ▒▒ ░   ░     ░ ░  ░░ ░▒  ░ ░   
 ░ ░  ░   ░   ▒      ░   ░ ░   ░         ░   ░  ░  ░     ░ ░   ░   ░   ▒    ░         ░   ░  ░  ░     
   ░          ░  ░         ░             ░  ░      ░           ░       ░  ░           ░  ░      ░     
 ░                                                                                                    
____________________________________________________________________________________________________

License: GNU 3.0 | AUTOR: Jorge Coronado | Twitter: @JorgeWebsec | Contact: jorgewebsec[@] gmail.com
____________________________________________________________________________________________________

Version: 1.0 | 17/04/2020 | Description: Search engines and add new BuscadorTelefono.py
Version: 1.1 | 10/05/2020 | Description: parser in URLS and graph report generator
Version: 1.2 | 01/06/2020 | Description: add facebook search and to correct bugs
Version: 1.2.1 | 04/06/2020 | Description: bug fixes, add INEapellidos and Dogpile in BuscadorPersonas
Version: 1.3 | 15/06/2020 | Description: add BuscadorNoticiasFalsas.py
Version: 1.4.0 | 22/06/2020 | Description: add generate log and add rtve in fact-checking domain
Version: 1.4.1 | 30/07/2020 | Description: add downloader pdf in BuscadorPersonas.py
Version: 1.5.0 | 22/08/2020 | Description: add personal data parser on Wikipedia in BuscadorPersonas
Version: 1.5.1 | 30/08/2020 | Description: added corruption keyword list 
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

"""

