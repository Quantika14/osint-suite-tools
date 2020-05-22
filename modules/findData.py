import modules.control as control
import modules.config as config
import os
from subprocess import call

def clean_empresa(empresa):
    empresa = empresa.split(" ")
    
    empresa_end = ""
    if len(empresa) > 2:
        for x in range(0, len(empresa)-1):
            empresa_end = empresa_end + " " + empresa[x]
        return empresa_end
    else:
        e_2 = empresa[1]
        return empresa[0]+ " " + e_2[0]

def search_and_find_data(n, ap1, ap2):
    if "win" in control.systemDetect():
        print("[!][WARNING][>] Esta funcionalidad solo está disponible en Linux...")

    if "linux" in control.systemDetect():
        print("")
        print("[---------------------BÚSQUEDA LOCAL DE ARCHIVOS-----------------------------]")
        print("|----[INFO][>] Thread 1: puede tardar varios minutos...")
        print("")

        #Buscamos los dos apellidos en minusculas
        print("|----[INFO][ARCHIVOS][DATA LOCAL][>] Buscando por apellidos...")
        target = "'" + ap1.lower() + " " + ap2.lower() + "'"
        os.system("pdfgrep " + target + " -ni data/ -r")


        #Buscamos los dos apellidos en mayusculas
        print("|----[INFO][ARCHIVOS][DATA LOCAL][>] Buscando por apellidos mayusculas...")
        target = "'" + ap1.upper() + " " + ap2.upper() + "'"
        os.system("pdfgrep " + target + " -ni data/ -r")

def search_adjudicaciones(empresa):
    #Buscamos la empresa en adjudicaciones
    empresa = clean_empresa(empresa)
    print("|----[INFO][>] Buscando la empresa " + empresa + " en data...")
    os.system("pdfgrep '" + empresa + "' -ni data/Adjudicaciones/ -r")

def search_investigados_condenados_politicosSpain(nombre, apellido1):
    #Limpiamos lso datos de entrada
    nombre = nombre.lower().strip()
    apellido1 = apellido1.lower().strip().replace("\n", "")


    #Buscamos si aparece en la lista de corruptos politicos
    f = open(config.politicosSpain_investigados, "r")
    for line in f.readlines():

        if nombre.lower() in line.lower() and apellido1.lower() in line.lower():
            print("|----[INFO][>] Se ha encontrado en la lista de investigados o condenados políticos: ")
            print("|--------[DATA][>] " + str(line))
            print("|--------[FUENTE][>] https://es.wikipedia.org/wiki/Anexo:Pol%C3%ADticos_de_Espa%C3%B1a_implicados_en_casos_judiciales")
    f.close()

#*******************************************************************
#FUNCIONES PARA BUSCADOR DE TELEFONOS
#*******************************************************************