from newspaper import Article
from search_engines import Google

import modules.parsers as parser

import requests
from pymongo import MongoClient

#Conexión con la base de datos
con = MongoClient()
db = con.Test

def news_parser(url, target):

    #Descargamos la noticia
    article = Article(url, language = 'es')
    article.download()

    #Parseamos la noticia
    article.parse()

    #La guardamos e imprimimos
    print(f"|----[INFO][WEB][>] {article.title}")
    print(f"|--------[INFO][WEB][AUTHORS][>] {article.authors}")
    print(f"|--------[INFO][WEB][PUBLISH DATE][>] {article.publish_date}")

    parser.parser_email(article.text)
    parser.parser_DNI(article.text)
    parser.parser_IBAN(article.text)
    parser.parser_n_tlfn(article.text)
    parser.FC_words_in_text(article.text)
    print(f"|--------[INFO][WEB][URL][>] {url}")

    news_insertMongoDB(target, url, article.title, article.authors, article.text, article.publish_date, article.top_image, article.movies, article.html)

    

def news_insertMongoDB(target, url, title, autor, text, date, top_image, movies, html):

    data = {"target": target, "url":url, "title":title, "autor":autor, "text":text, "date":date, "top_image":top_image, "movies":movies, "html":html}

    x = db.DG.find_one({"url":url})

    if x:
        print(f"|----[DB][>] Found URL in DB -> {url}")
        pass
    else:
        db.DG.insert(data)
        print(f"|----[DB][>] Insert INFO in DB-> {url}")
