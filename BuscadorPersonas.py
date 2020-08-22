'''
Copyright (c) 2020, QuantiKa14 Servicios Integrales S.L
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
'''

#AUTHOR: JORGE WEBSEC
import wikipedia, wikipediaapi, requests, json, re, os, wget
from bs4 import BeautifulSoup
from search_engines import Dogpile
from search_engines import Google
from tldextract import extract

import modules.er as er
import modules.control as control
import modules.parsers as parser
import modules.findData as findData_local
import modules.config as config
import modules.graph as graph
import modules.spainpress as spainpress
import modules.facebook as facebook
import modules.ine_nombreApellidos as INEapellidos

def get_PersonalData_Wikipedia(target):

    try:
        wiki_wiki = wikipediaapi.Wikipedia('es')
        page_py = wiki_wiki.page(target)
        
        URL = page_py.canonicalurl
        HTML = requests.get(URL)
        parser.extract_personalData_wikipedia(HTML)
    except:
        pass

#Funciones para buscar en BORME
def parserLibreborme_json(j):
    print()
    print("|----[INFO][CARGOS EN EMPRESAS ACTUALMENTE][>] ")
    for cargos_actuales in j["cargos_actuales"]:
        print("    - Desde: " + cargos_actuales["date_from"] + " hasta la actualidad.")
        print("    - Empresa: " + cargos_actuales["name"])
        print("    - Cargo: " + cargos_actuales["title"])

        if cargos_actuales["name"]:

            print("|----[INFO][LOCAL DATA][Adjudicaciones][>] Este proceso puede tardar...")
            #findData_local.search_adjudicaciones(cargos_actuales["name"])

        config.companiesData_list.append(cargos_actuales["name"])

    print()
    print("|----[INFO][CARGOS EN EMPRESAS HISTORICOS][>] ")
    for cargos_historicos in j["cargos_historial"]:
        try:
            print("    - Desde: " + cargos_historicos["date_from"])
        except:
            pass
        print("    - Hasta: " + cargos_historicos["date_to"])
        print("    - Empresa: " + cargos_historicos["name"])
        print("    - Cargo: " + cargos_historicos["title"])
        
        if cargos_historicos["name"]:
            
            print("|----[INFO][LOCAL DATA][Adjudicaciones][>] Este proceso puede tardar...")
            #findData_local.search_adjudicaciones(cargos_historicos["name"])

        config.data_list.append(cargos_historicos["name"])

    print("|----[FUENTES][BORME][>] ")
    for boe in j["in_bormes"]:
        print("    - CVE: " + boe["cve"])
        print("    - URL: " + boe["url"])

def searchLibreborme(apellidos, nombre):
    try:
        URL = "https://libreborme.net/borme/api/v1/persona/" + apellidos.replace(" ", "-") + "-" + nombre.replace(" ", "-") + "/"
        html = requests.get(URL)
        html_text = html.text

        if len(html_text)>1:
            
            j = json.loads(html.text)
            parserLibreborme_json(j)
            
        else:
            URL = "https://libreborme.net/borme/api/v1/persona/" + nombre.replace(" ", "-") + "-" + apellidos.replace(" ", "-") + "/"
            html = requests.get(URL)
            try:
                j = json.loads(html.text)
                parserLibreborme_json(j)

            except:
                print("|----[INFO][EMPRESAS][>] No aparecen resultados en el BORME.")
    except:
        print("|----[INFO][EMPRESAS][>] No aparecen resultados en el BORME.")

#Funciones para buscar en Wikipedia
def searchWikipedia(target):

    try:
        wikipedia.set_lang("es")
        d0 = wikipedia.search(target)

        if d0:
            print()
            print("|----[INFO][WIKIPEDIA][>] ")
            print("     |----[INFO][SEARCH][>] ")
            print("     - Resultados encontrados: ")
            for r in d0:
                print("     - " + r)
        else:
            print("|----[INFO][WIKIPEDIA][>] No aparecen resultados en WIKIPEDIA.")

    except:
        print("[!][WARNING][WIKIPEDIA][>] Error en la API...")

    try:
        d1 = wikipedia.page(target)

        linksWIKI = d1.links
        urlWIKI = d1.url

        if d1:
            print("     |----[INFO][TAGS][>] ")
            for l in linksWIKI:
                print("     - " + l)
            print("|----[FUENTES][WIKIPEDIA][>] ")
            print("     - " + urlWIKI)
            config.wikipediaData_list.append(urlWIKI)
        else:
            print("|----[INFO][WIKIPEDIA][>] No aparecen resultados en WIKIPEDIA.")
    
    except:
        print("[!][WARNING][WIKIPEDIA][>] Error en la API o no aparecen resultados...")

#Funciones para buscar en Youtube
def searchYoutube(target):
    URL = "https://www.youtube.com/results?search_query="
    html = requests.get(URL + target).text

    soup = BeautifulSoup(html, "html.parser")
    vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
    vids_titles = soup.findAll("div", attrs={'class', 'style-scope ytd-video-renderer'})

    videolist = config.youtubeData_list

    for v in vids:
        tmp = 'https://www.youtube.com' + v['href']
        videolist.append(tmp)
    
    print()
    print("|----[INFO][YOUTUBE][>] ")
    for v in vids_titles:
        print("     - " + v)
        print(html)
    print("|----[FUENTES][YOUTUBE][>] ")
    for u in videolist:
        print("     - " + u)

#Funciones para buscar en las Páginas Amarillas
def cleanPaginasAmarillas_result(r):
    r_array = r.split("Ver mapa")

    r2_array = r_array[0].split("Imprimir Ficha")
    r = r2_array[2].split()

    return r

#Funcion para buscar en página amarilla
def searchPaginasAmarillas(nombre, a1, a2, loc):
    url = "http://blancas.paginasamarillas.es/jsp/resultados.jsp?no=" + nombre + "&ap1=" + a1 + "&ap2=" + a2 + "&sec=41&pgpv=1&tbus=0&nomprov=" + loc + "&idioma=spa"

    html = requests.get(url).text

    soup = BeautifulSoup(html, "html.parser")
    r = soup.find("div", attrs={'class': 'resul yellad yellad_ad0'})
    r = er.remove_tags(str(r))

    if not r == "None":
        print("|----[INFO][PAGINAS AMARILLAS][>] ")
        print("     - " + str(cleanPaginasAmarillas_result(r)))
    else:
        pass

def search_google_and_downloadPDF(target):

    print("|--[INFO][>] Now we are going to download the PDF files where the target appears...")

    #Creamos una carpeta con el nombre del target y nos movemos
    name_dir = target.replace(" ", "-")
    if os.path.isdir(f"data/{name_dir}"):
        os.chdir(f"data/{name_dir}")
    else:
        os.mkdir(f"data/{name_dir}")
        os.chdir(f"data/{name_dir}")

    engine = Google()
    results = engine.search(f"filetype:pdf intext:'{target}' ")
    for r in results:
        print ("|--[INFO][GOOGLE][RESULTS][>] " + r["title"])
        print ("|----[INFO[DESCRIPTION][>] " + r["text"])
        print ("|----[INFO][LINK][>] " + r["link"])

        try:
            filename = wget.download(r["link"])
            print ("|----[INFO][GOOGLE][DOWNLOAD][>] " + filename)
        except Exception as e:
            print ("|----[ERROR][>] " + str(e))
            pass
    
    os.chdir(f"../../")

#Funcion para buscar en Google
def search_google_(target):
    engine = Google()
    results = engine.search("'" + target + "'")
    for r in results:
        print ("|--[INFO][GOOGLE][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"])
        
        try:
            tsd, td, tsu = extract(r["link"])
            domain = td + '.' + tsu

            web = requests.get(r["link"], timeout=3)
            print ("|----[INFO][WEB][HTTP CODE][>] " + str(web.status_code) + "\n")

            if web.status_code >= 200 or web.status_code < 300:

                if not domain in config.BL_parserPhone:
                    TEXT = er.remove_tags(str(web.text))
                    parser.parserMAIN(TEXT)

        except Exception as e:
            print ("|----[ERROR][HTTP CONNECTION][>] " + str(e))

def search_dogpile_(target):
    engine = Dogpile()
    results = engine.search("'" + target + "'")
    for r in results:
        print ("|--[INFO][DOGPILE][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"])
        
        try:
            web = requests.get(r["link"], timeout=3)
            print ("|----[INFO][WEB][HTTP CODE][>] " + str(web.status_code) + "\n")
            if web.status_code >= 200 or web.status_code < 300:
                TEXT = er.remove_tags(str(web.text))
                parser.parserMAIN(TEXT)

        except Exception as e:
            print ("|----[ERROR][HTTP CONNECTION][>] " + str(e))


def graphGenerator_Companies(target):
    graph.get_GraphNodePersonalData(target)

def banner():
    print(config.banner)

def menu():
    print("__________________________________________________")
    print("| 1. Name and surnames                           |")
    print("| 2. Name, surnames and city                     |")
    print("| 3. Search names and surnames in list           |")
    print("|________________________________________________|")
    print()

    m = int(input("Select 1/2/3: "))
    if m == 1:
        
        nombre = input("Insert name: ")
        apellido1 = input("Insert surname (only one): ")
        apellido2 = input("Insert second surname: ")


        #Buscamos si aparece en la lista de politicos investigados o condenados
        findData_local.search_investigados_condenados_politicosSpain(nombre, apellido1)

        #Target sin filtrar
        target_no_clean = nombre + " " + apellido1 + " " + apellido2

        #Limpiamos de acentos
        nombre_ = er.replace_acentos(nombre)
        apellido1_ = er.replace_acentos(apellido1)
        apellido2_ = er.replace_acentos(apellido2)

        #Limpiamos de letras raras
        nombre_ = er.replace_letras_raras(nombre_)
        apellido1_ = er.replace_letras_raras(apellido1_)
        apellido2_ = er.replace_letras_raras(apellido2_)

        target = nombre_ + " " + apellido1_ + " " + apellido2_
        apellidos_ = apellido1_ + " " + apellido2_
        
        #LANZADERA DE FUNCIONES
        INEapellidos.searchApellidos(nombre, apellido1, apellido2)
        searchWikipedia(target)
        get_PersonalData_Wikipedia(target_no_clean)
        searchLibreborme(apellidos_, nombre_)
        searchYoutube(target)
        spainpress.search_abc_es(target)
        facebook.get_postsFB(target)

        #Buscadores
        m = input("Do you want to search with your name in search engines like Google and DogPile? [Y/n]")
        if m == "y" or m == "Y":
            search_google_(target)
            search_dogpile_(target)
        else:
            print ("|----[END][>] Author's message: 'Google knows much more information than you think'")

        #Descargamos PDFs
        m = input("Do you want to download pdf files of the target? [Y/n]")
        if m == "y" or m == "Y":
            search_google_and_downloadPDF(target)
        else:
            print ("|----[END][>] Author's message: 'PDFs are a mine of information. You miss it'")

        #Creamos grafo
        m = input("Do you want a report? [Y/n]")
        if m == "y" or m == "Y":
            graphGenerator_Companies(target)
        else:
            print ("|----[END][>] Author's message: 'In times of crisis the intelligent seek solutions and the useless culprits'")

        #findData_local.search_and_find_data(nombre_, apellido1_, apellido2_)

    if m == 2:
        nombre = input("Insert name: ")
        apellido1 = input("Insert surname (only one): ")
        apellido2 = input("Insert second surname: ")
        loc = input("Insert city: ")

        #Target sin filtrar
        target_no_clean = nombre + " " + apellido1 + " " + apellido
        
        #Buscamos si aparece en la lista de politicos investigados o condenados
        findData_local.search_investigados_condenados_politicosSpain(nombre, apellido1)

        #Limpiamos de acentos
        nombre = er.replace_acentos(nombre)
        apellido1 = er.replace_acentos(apellido1)
        apellido2 = er.replace_acentos(apellido2)
        loc = er.replace_acentos(loc)

        #Limpiamos de letras raras
        nombre = er.replace_letras_raras(nombre)
        apellido1 = er.replace_letras_raras(apellido1)
        apellido2 = er.replace_letras_raras(apellido2)
        loc = er.replace_letras_raras(loc)

        target = nombre + " " + apellido1 + " " + apellido2
        apellidos = apellido1 + " " + apellido2
        
        #LANZADERA DE FUNCIONES
        INEapellidos.searchApellidos(nombre, apellido1, apellido2)
        get_PersonalData_Wikipedia(target_no_clean)
        searchWikipedia(target)
        searchLibreborme(apellidos, nombre)
        searchYoutube(target)
        searchPaginasAmarillas(nombre, apellido1, apellido2, loc)
        search_google_(target)
        spainpress.search_abc_es(target)
        facebook.get_postsFB(target)
        search_google_and_downloadPDF(target)

        print("")
        print("[--------------------------------------------------]")
        print("")
        findData_local.search_and_find_data(nombre, apellido1, apellido2)

    if m == 3:
        print("[INFO][NAMES AND SECONDS NAMES LIST][>] by default is 'targets.txt'...")
        print("[INFO][NAMES AND SECONDS NAMES LIST][>] If you want to change it: modules/config.py")
        file_ = open(config.target_list, 'r')
        for target in file_.readlines():
            
            name_target = target.replace("||", " ").strip()
            print("|----[TARGET][>] " + name_target)
            #Buscamos su edad y fallecimiento en Wikipedia
            get_PersonalData_Wikipedia(name_target)

            target_ = target.split("||")
            nombre = target_[0]
            apellido1 = target_[1]
            

            #Buscamos si aparece en la lista de politicos investigados o condenados
            findData_local.search_investigados_condenados_politicosSpain(str(nombre), str(apellido1))

            #Buscamos en el BORME
            searchLibreborme(apellido1, nombre)
        file_.close()

def main():
    banner()
    menu()
    
if __name__ == "__main__":
    main()
