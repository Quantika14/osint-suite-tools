import re, requests
from bs4 import BeautifulSoup
import modules.config as config
import modules.er as er
import modules.mongo as mongo
import modules.data as data

def parser_email(text):

	r = re.compile(r"[a-z0-9!#$%&'*+-/=?^_`{|}~]{1,64}@[a-zA-Z0-9]{1,255}\.[a-zA-Z0-9-]{1,24}")
	results = r.findall(text)
	if results:
		for x in results:
			x = er.replace_acentos(er.remove_tags(er.replace_letras_raras(str(x))))
			print("|--------[INFO][PARSER][EMAIL][>] " + x)
			if len(x) <20:
				config.emailsData_list.append(x)

def parser_n_tlfn(text):


	all_matches_telf = re.compile(r"(?:(?:\+(?:[0]{0,4})?)?34[. -]{0,3})?[6789][0-9]{2}[ ]{0,3}(?:[0-9][ ]?){5}[0-9]")
	
	'''
		Fuentes para buscar patrones:
		.............................

		https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s03.html
		https://zadarma.com/es/tariffs/numbers/latvia/riga/
		http://www.asifunciona.com/tablas/pref_telefonos/pref_telefonos_1.htm
		https://en.wikipedia.org/wiki/List_of_mobile_telephone_prefixes_by_country
	'''
	international_numbers = re.compile(r"\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}")

	results_spain = all_matches_telf.findall(text)
	results_international = international_numbers.findall(text)


	for x in results_spain:
		print("|--------[INFO][PARSER][SPAIN][NUMBER PHONE][>] " + x)
		config.phonesData_list.append(x)
	list(set(config.phonesData_list))
	
	for x in results_international:
		print("|--------[INFO][PARSER][INTERNACIONAL][NUMBER PHONE][>] " + x)
		#config.phonesData_list.append(x)

def parser_IBAN(text):

	r = re.compile(r"[a-zA-Z]{2}[0-9]{0,2}[ ]?([0-9]{4}[ ]?){5}")
	results = r.findall(text)
	if results:
		for x in results:
			print ("|--------[INFO][PARSER][IBAN][>] " + str(x))
		

def parser_DNI(text):
	
	r = re.compile(r"(^[0-9]{8,8}[A-Za-z]$)")
	results = r.findall(text)
	if results:
		for x in results:
			print ("|--------[INFO][PARSER][DNI][>] " + str(x))
			config.DNIData_list.append(str(x))

def FC_words_in_text(text):

	for w in config.FC_corruption_keywords:

		if w in text.lower():

			print(f"|--------[INFO][PARSER[CORRUPTION KEYWORD][WORD][>] Word detected: {w}!")

	for w in config.FC_words_list:

		if w in text.lower():

			print(f"|--------[INFO][PARSER[FACT-CHECKING][WORD][>] Word detected: {w}!")

def extract_personalData_wikipedia(html, url, target):
	
	soup = BeautifulSoup(html.text, "html.parser")

	tables = soup.findAll("tr")
	for tr in tables:
		tr_ = er.remove_tags(str(tr))
		if "Nacimiento" in tr_:
			print (f"|----[INFO][AGE][>] Age found on Wikipedia {tr_}")
			
			#Obtenemos el horoscopo
			signo = ("capricornio", "acuario", "piscis", "aries", "tauro", "géminis", "cáncer", "leo", "virgo", "libra", "escorpio", "sagitario")
			meses = {"enero":1, "febrero":2, "marzo":3, "abril":4, "mayo":5, "junio":6, "julio":7, "agosto":8, "septiembre":9, "octubre":10, "noviembre":11, "diciembre":12}
			fechas = (20, 19, 20, 20, 21, 21, 22, 22, 22, 22, 22, 21)
			dia = 0
			mes = 0
			
			words = tr_.replace("\n", " ").split(" ")

			for w in words:

				if w.isdigit() and len(w)<=2:
					dia = int(w)
				else:
					pass
				
				if w.lower() in meses.keys():
					mes = meses.get(w.lower())
				else:
					pass

			mes=mes-1
			if dia>fechas[mes]:
				mes=mes+1
			if mes==12:
				mes=0
				
			print ("|----[INFO][HOROSCOPO][>] " + signo[mes])

			#Save to DB
			birth = tr_.replace("Age found on Wikipedia Nacimiento", "")
			mongo.personalData_Wikipedia_insertMongoDB(target, birth, url, 1)
			mongo.personalData_Wikipedia_insertMongoDB(target, signo[mes], url, 3)
			data.Wiki_birth = birth
			data.Wiki_url = url
			data.WIki_horoscopo = signo[mes]

		if "Fallecimiento" in tr_:
			print (f"|----[INFO][DEATH][>] Death found on Wikipedia {tr_}")

			#Save to DB
			mongo.personalData_Wikipedia_insertMongoDB(target, tr_, url, 2)
			data.Wiki_death = tr_
		
		if "Partido político" in tr_:
			print (f"|----[INFO][POLITICAL PARTY][>] {tr_}")

			#Save to DB
			mongo.personalData_Wikipedia_insertMongoDB(target, tr_, url, 7)
			data.Wiki_politicalParty = tr_
		
		if "Ocupación" in tr_:
			print (f"|----[INFO][EMPLOYMENT][>] {tr_}")

			#Save to DB
			mongo.personalData_Wikipedia_insertMongoDB(target, tr_, url, 4)
			data.Wiki_employment = tr_.replace("Ocupación", "")
		
		if "Religión" in tr_:
			print (f"|----[INFO][RELIGION][>] {tr_}")

			#Save to DB
			mongo.personalData_Wikipedia_insertMongoDB(target, tr_, url, 5)
			data.Wiki_religion = tr_
		
		if "Hijos" in tr_:
			print (f"|----[INFO][SONS][>] {tr_}")

			#Save to DB
			mongo.personalData_Wikipedia_insertMongoDB(target, tr_, url, 6)
			data.Wiki_sons = tr_
		


def parserMAIN(text):

	parser_email(text)
	parser_DNI(text)
	parser_IBAN(text)
	#parser_n_tlfn(text)
	FC_words_in_text(text)