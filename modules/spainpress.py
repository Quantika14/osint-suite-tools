import requests
from bs4 import BeautifulSoup

import modules.er as er

def search_abc_es(target):

        target = target.replace(" ", "+")
        target_split = target.split("+")

        try:
                url = f"https://abc.es/hemeroteca/resultos-busqueda-avanzada/todo?exa={target}"

                HTML = requests.get(url).text

                soup = BeautifulSoup(HTML, "html.parser")
                results = soup.findAll("a",attrs={"class": "titulo"})
                if results:
                        for r in results:
                                print ()
                                print ("|----[INFO][SPAINPRESS][ABC][>]")
                                print ("|--------[TITLE][>] " + er.remove_tags(str(r)))
                                print ("|--------[URL][>]" + r["href"])
                else:           
                        print ()
                        print("|----[INFO][SPAINPRESS[ABC][>] No record found...")
        
        except Exception as e:
               print ()
               print (f"|----[WARNING][ABC ERROR][>] {e}") 