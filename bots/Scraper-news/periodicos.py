from bs4 import BeautifulSoup
import ssl, urllib, os, re, requests, sys, spacy, threading
from urllib.parse import urlparse
from color import Color
from language import Language
from collections import Counter
from config import DB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import svm


class Noticia():
    ''' Datos necesarios para guardar en bbdd mas score para filtro'''

    def __init__(self, url=None, text=None, title=None):
        self.url = url
        self.text = text
        self.title = title


class Periodicos():
    def __init__(self, db_con=None, lang='ES'):
        self.__colores = Color()
        self.__db_con = db_con
        self.__lang = lang
        self.__phrases = Language(lang).getPhrases()
        self.__lock = threading.Lock()
        self.__periodicos = self.__getDict(lang)
        self.__results = []

    def __getDict(self, lang):
        dict = {}
        with open(f'./archivos/news-{lang}.txt'.lower()) as file:
            lines = file.read().splitlines()
        for line in lines:
            valores = line.split('=')
            dict[valores[0]] = valores[1]
        return dict

    def load_newspapers(self):
        ''' Por si se quiere el diccionario de periodico-clase creado '''

        return list(self.__periodicos.keys())

    def __fix_url(self, url, href):
        ''' Parser de urls '''

        getElem = href.find("#")
        if 'http://' in href.lower() or 'https://' in href.lower():
            if getElem != -1:
                return href[:getElem]
            else:
                return href
        elif 'http:/' in href.lower() or 'https:/' in href.lower():
            if getElem != -1:
                return f'{url}{href[href.find("/", 7) + 1:getElem]}'
            else:
                return f'{url}{href[href.find("/", 7) + 1:]}'
        else:
            if getElem != -1:
                return urllib.parse.urljoin(url, href[:getElem])
            else:
                return urllib.parse.urljoin(url, href)

    def __scraper(self, url):
        ''' Creamos headers y un contexto de ssl para evitar errores o bloqueos
            Luego hacemos una peticion get a la url y devolvemos el objeto bs
        '''

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context
        html = requests.get(url, headers=header).content
        return BeautifulSoup(html, 'html.parser', from_encoding="iso-8859-1")

    def __search_text(self, soup, css_class):
        ''' Buscamos la clase que contiene la noticia, y cogemos su texto'''

        tag = soup.select(f"[class='{css_class}']")
        if tag:
            tag = tag[0]
            ps = tag.find_all('p', recursive=False)
            if ps:
                result = ' '.join([p.text for p in ps])
                return result
            else:
                ps = tag.find_all('p')
                result = ' '.join([p.text for p in ps])
                return result

    def __search_title(self, soup):
        ''' Recogemos titulo y eliminamos simbolos raros del final '''
        title = soup.title.string
        busqueda = re.search('[\|\#\[\]\{\}\$-]', title)
        if busqueda:
            end_title = str(title[:busqueda.start()])
            end_title = end_title.replace('\n', '').replace('\t', '').replace('\r', '').strip()
            return end_title
        else:
            return str(title).replace('\n', '').replace('\t', '').replace('\r', '').strip()


    def __process(self, url, css):
        ''' Procesamos una noticia a través de su url'''

        soup_new = self.__scraper(url)
        text = self.__search_text(soup_new, css)
        title = self.__search_title(soup_new)
        return (soup_new, text, title)


    def __worker(self, url, css_class):
        '''
        Recorremos todos los link buscando las palabras en estos, y los que las contengan,
        nos recorremos la noticia y la recogemos. Por ultimo damos por defecto la que mas
        palabras contenga de las buscadas. Si no es esta doy la opción de escoger una de las otras.
        :param words: palabras a buscar
        :param url: url de la que tiramos
        :param css_class: clase de html
        :return:
        '''

        soup = self.__scraper(url)
        news = []
        urlsScrapeadas = set()
        tagsFiltered = [a for a in soup.find_all('a') if a.get('href')]
        for a in tagsFiltered:
            try:
                urlfixed = self.__fix_url(url, str(a.get('href').replace(" ", "")))

                if url in urlfixed and not urlfixed in urlsScrapeadas:
                    urlsScrapeadas.add(urlfixed)
                    soup_new, text, title = self.__process(urlfixed, css_class)

                    if text:
                        new = Noticia(title=title, text=text, url=urlfixed)
                        print(f'Añadimos a nuestros periodicos: {urlfixed}')
                        news.append(new)
            except Exception:
                pass
        print(f'Añadimos un total de {len(news)} desde {url}')
        self.__results.extend(news)

    def search(self):
        '''
                Cogemos un mapa de periodicos con las clases que hay que buscar,
                y llamamos a los threads para que busquen las noticias.
                Devolvemos una lista con todos los objetos Noticia recolectados
                '''
        threads = []
        for url, css_class in self.__periodicos.items():
            threads.append(threading.Thread(target=self.__worker, args=(url, css_class)))
            threads[-1].start()

        # Esperamos a que todos los thread hayan terminado
        for thread in threads:
            thread.join()

        return self.__results
