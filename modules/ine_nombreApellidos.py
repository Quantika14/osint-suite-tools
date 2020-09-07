import csv
import modules.data as data

def searchApellidos(nombre, a1, a2):
    with open('data/spanish-names-master/hombres.csv', newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines: 

            if nombre.upper() == row[0]:
                print (f"|----[INFO][{nombre.upper()}][>] Frequency as a man's name is {row[1]} in Spain")
                data.INE_name_man = row[1]
    
    with open('data/spanish-names-master/mujeres.csv', newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines: 

            if nombre.upper() == row[0]:
                print (f"|----[INFO][{nombre.upper()}][>] Frequency as a woman's name is {row[1]} in Spain")
                data.INE_name_woman = row[1]

    with open('data/spanish-names-master/apellidos.csv', newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            if a1.upper() == row[0]:
                print (f"|----[INFO][{a1.upper()}][>] Frequency as surname: {row[1]} in Spain")
                data.INE_surname = {row[1]}
            if a2.upper() == row[0]:
                print (f"|----[INFO][{a2.upper()}][>] Frequency as second surname: {row[2]} in Spain")
                data.INE_second_surname = row[1]
