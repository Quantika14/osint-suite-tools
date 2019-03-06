#!/usr/bin/env python
# -*- coding: utf-8 -*

import modules.control as control
import os

def search_and_find_data(n, ap1, ap2):
    if "win" in control.systemDetect():
        print "[!][WARNING][>] Esta funcionalidad solo está disponible en Linux..."
    if "linux" in control.systemDetect():


        #Buscamos los dos apellidos en minusculas
        print "|----[INFO][ARCHIVOS][DATA LOCAL][>] Apellidos en minus..."
        command1 = "pdfgrep '" + ap1.lower() + " " + ap2.lower() + "' -R"
        exe_find = os.system(command1)
        print exe_find

        #Buscamos los dos apellidos y el nombre en minusculas
        print "|----[INFO][ARCHIVOS][DATA LOCAL][>] Apellidos y nombre en minus..."
        command2 = "pdfgrep '" + ap1.lower() + " " + ap2.lower() + " " + n.lower() + "' -R"
        exe_find = os.system(command2)
        print exe_find

        #Buscamos los dos apellidos en mayusculas
        print "|----[INFO][ARCHIVOS][DATA LOCAL][>] Apellidos en Mayus"
        command1 = "pdfgrep '" + ap1.upper() + " " + ap2.upper() + "' -R"
        exe_find = os.system(command1)
        print exe_find

        #Buscamos los dos apellidos y el nombre en mayusculas
        print "|----[INFO][ARCHIVOS][DATA LOCAL][>] Apellidos y nombre en Mayus"
        command2 = "pdfgrep '" + ap1.upper() + " " + ap2.upper() + " " + n.upper() + "' -R"
        exe_find = os.system(command2)
        print exe_find

