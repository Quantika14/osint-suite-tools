#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os

def systemDetect():
    sistemaop = sys.platform
    return sistemaop

def countFiles_data():
    if "win" in systemDetect():
        print("[!][WARNING][>] Recomendamos el uso de Linux...")
    if "linux" in systemDetect():
        f_count = os.system("ls -A | wc -l")
        if f_count < 10000:
            print("[*][LOCAL][>] Actualmente su low data es de: " + str(f_count))
        else:
            print("[*][LOCAL][>] Actualmente su big data es de: " + str(f_count))
