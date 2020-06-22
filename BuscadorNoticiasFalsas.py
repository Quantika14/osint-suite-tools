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
from bs4 import BeautifulSoup
import requests, re, time
from datetime import datetime
from search_engines import Google
from search_engines import Duckduckgo
from tldextract import extract
from difflib import SequenceMatcher


import modules.config as config
import modules.er as er
import modules.parsers as parser
import modules.twitter as Twint


def generateLOG(data, title):

    f = open(f"report/report-{title[:10]}", "a")

    f.write(data)

    f.close()

def footprintingWEB_TITLE(HTML):

    soup = BeautifulSoup(HTML.text, "html.parser")

    TITLE = soup.title.string

    return TITLE

def footprintingWEB_DESC(HTML):

        soup = BeautifulSoup(HTML.text, "html.parser")

        description = soup.find("meta",  property="og:description")
        return description

def compareTEXT(TEXT_0, TEXT):

    m = SequenceMatcher(None, TEXT_0, TEXT)
    ratio = m.ratio()

    return ratio

#Funcion para buscar en Google
def search_google_(target, TEXT_0):

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
                if ".pdf" in r["link"]:
                    pass
                else:
                    if not domain in config.BL_parserPhone:
                        TEXT = er.remove_tags(str(web.text))
                        parser.parserMAIN(TEXT)
                        parser.FC_words_in_text(TEXT)

                        ratio = compareTEXT(TEXT_0, TEXT)
                        print(f"|----[INFO][COMPARE TEXTS][>] Ratio: {ratio}")

                        #Guardamos la info en un log
                        data = f"{r['title']} ||| {r['link']} ||| {r['text']}, ||| {ratio} \n"
                        generateLOG(data, target)

                    else:
                        pass
            print("")

        except Exception as e:
            print ("|----[ERROR][HTTP CONNECTION][>] " + str(e))

def search_DDG_(target, TEXT_0):

    engine = Duckduckgo()
    results = engine.search("'" + target + "'")
    for r in results:
        print ("|--[INFO][GOOGLE][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"])
        
        try:
            tsd, td, tsu = extract(r["link"])
            domain = td + '.' + tsu

            web = requests.get(r["link"], timeout=3)
            print ("|----[INFO][WEB][HTTP CODE][>] " + str(web.status_code) + "\n")

            if web.status_code >= 200 or web.status_code < 300:
                if ".pdf" in r["link"]:
                    pass
                else:
                    if not domain in config.BL_parserPhone:
                        TEXT = er.remove_tags(str(web.text))

                        compareTEXT(TEXT, TEXT_0)
                        parser.FC_words_in_text(TEXT)
                        parser.parserMAIN(TEXT)

                        ratio = compareTEXT(TEXT_0, TEXT)
                        print(f"|----[INFO][COMPARE TEXTS][>] Ratio: {ratio}")
                        
                        #Guardamos la info en un log
                        data = f"{r['title']} ||| {r['link']} ||| {r['text']}, ||| {ratio} \n"
                        generateLOG(data, target)

                    else:
                        pass
            print("")
            time.sleep(2)

        except Exception as e:
            print ("|----[ERROR][HTTP CONNECTION][>] " + str(e))

def search_DDG_DORKS(TITLE, TEXT_0):


    engine = Duckduckgo()
    for FC_domain in config.FC_list:

        results = engine.search(f"site:{FC_domain} {TITLE}")
        for r in results:
            print ("|--[INFO][GOOGLE][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"])
            
            try:
                
                tsd, td, tsu = extract(r["link"])
                domain = td + '.' + tsu

                web = requests.get(r["link"], timeout=3)
                print ("|----[INFO][WEB][HTTP CODE][>] " + str(web.status_code) + "\n")

                if web.status_code >= 200 or web.status_code < 300:
                    if ".pdf" in r["link"]:
                        pass
                    else:
                        if not domain in config.BL_parserPhone:
                            TEXT = er.remove_tags(str(web.text))

                            compareTEXT(TEXT, TEXT_0)
                            parser.FC_words_in_text(TEXT)
                            parser.parserMAIN(TEXT)

                            ratio = compareTEXT(TEXT_0, TEXT)
                            print(f"|----[INFO][COMPARE TEXTS][>] Ratio: {ratio}")
                        
                            #Guardamos la info en un log
                            data = f"{r['title']} ||| {r['link']} ||| {r['text']}, ||| {ratio} \n"
                            generateLOG(data, target)

                        else:
                            pass
                print("")
                time.sleep(2)
                
            except Exception as e:
                print ("|----[ERROR][HTTP CONNECTION][>] " + str(e))

def main():

    #Imprimimos el banner principal
    print(config.banner)

    #Insertamos la URL a buscar
    url = input("Insert URL: ")

    #Obtenemos el HTML
    HTML = requests.get(url)

    #Obtenemos el título
    TITLE = footprintingWEB_TITLE(HTML)

    #Obtenemos la descripción
    DESC = er.remove_tags(str(footprintingWEB_DESC(HTML))) 

    print(f"|----[TARGET][>] {url}")
    print (f"|--------[TARGET][TITLE][>] {TITLE}")
    print (f"|--------[TARGET][DESCRIPTION][>] {DESC}")
    time.sleep(2)

    #Obtenemos el texto de la noticia
    TEXT_0 = er.remove_tags(str(HTML.text))

    #buscamos una fecha en la URL
    DATE = parser.parser_EN_DATE(url)

    #Parseamos y obtenemos diferentes tipos de datos
    parser.parserMAIN(TEXT_0)
    time.sleep(3)

    #Buscamos en Google y DuckDuckGo
    print("|----[INFO][>] Now let's look for other news: \n")
    
    m = input("Do you want to search the original web? (Y/n): ")

    if m == "y" or m == "Y":
        search_google_(TITLE, TEXT_0)
        search_DDG_(TITLE, TEXT_0)
    else:
        pass

    #Buscamos en plataformas de verificación
    m = input("Do you want to analyze in fact-checking platforms? (Y/n): ")

    if m == "y" or m == "Y":

        #Buscamos con dorks en DDG
        search_DDG_DORKS(TITLE, TEXT_0)

    else:

        exit
    
    #Buscamos en Twitter
    m = input("Do you want to search in Twitter? (Y/n): ")
    
    if m == "y" or m == "Y":

        #Buscamos con dorks en DDG
        Twint.search_Twitter(url)

    else:

        exit

if __name__ == "__main__":
    main()