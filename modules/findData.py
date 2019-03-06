#!/usr/bin/env python
# -*- coding: utf-8 -*

import subprocess
from os import listdir
from PyPDF2 import PdfFileReader

#Funcion para realizar comandos en Windows
def cmd(commando):
    subprocess.run(commando, shell=True)

def search_and_find_data(target):
    f = open("data\/arbol.txt", "r")
    for l in f.readlines():
        text_extractor(l, target)

def text_extractor(path, target):
    

    for p in listdir(path):

        with open(p, 'rb') as f:
            pdf = PdfFileReader(f)
    
            number_of_pages = pdf.getNumPages()
            for i in range(1,number_of_pages):
                page = pdf.getPage(i)
                text = page.extractText()
                if target.upper() in text.upper():

                    print path