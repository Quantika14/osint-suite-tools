from bs4 import BeautifulSoup
import lxml, requests, re
from pymongo import MongoClient

#Conexión con la base de datos
con = MongoClient()
db = con.Dante

def insertBOE(ident, title, text):

    data = {"identificador": ident, "titulo":title, "texto":text}

    x = db.DG.find_one({"identificador":ident})

    if x:

        print(f"|----[DB][>] Found URL in DB -> {title}")
        pass
    else:

        db.DG_BOE.insert(data)
        print(f"|----[DB][>] Insert INFO in DB-> {title}")


# Eliminar tags HTML
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)

def generate_BOE(ano1, ano2, idI, idF):


	for ano in range(ano1,ano2):

		for id in range(idI, idF):

			BOE = "BOE-A-" + str(ano) + "-" + id

			extractBOE(BOE)

dif_count = 0

def extractBOE(BOE_id):
	global dif_count

	if dif_count < 1000:
		
		pass

	else:

		try:
			url_base = "https://boe.es/diario_boe/xml.php?id="

			#BOE_id = "BOE-A-2018-16868"

			url_end = url_base + BOE_id

			data = requests.get(url_end)

			soup = BeautifulSoup(data.content, "lxml")

			identificador = remove_tags(str(soup.find("identificador")))

			titulo = remove_tags(str(soup.find("titulo")))

			texto = remove_tags(str(soup.find("texto")))

			insertBOE(identificador, titulo, texto)
		
		except:
			dif_count += 1


def main():

	ano1 = input("Indicates the starting year: ")
	ano2 = input("Indicates the end year:")


main()
