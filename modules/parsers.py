import re
from bs4 import BeautifulSoup
import modules.config as config
import modules.er as er

def parser_email(text):

	r = re.compile(r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$)")
	results = r.findall(text)
	if results:
		for x in results:
			x = er.replace_acentos(er.remove_tags(er.replace_letras_raras(str(x))))
			print("|--------[INFO][PARSER][EMAIL][>] " + x)
			if len(x) <20:
				config.emailsData_list.append(x)

def parser_n_tlfn(text):

	#Para buscar dentro de un texto
	reg0 = re.compile("^\+(?:[0-9]●?){6,14}[0-9]$")
	#Para buscar con la extension
	reg1 = re.compile("^\+[0-9]{1,3}\.[0-9]{4,14}(?:x.+)?$")
	
	r0 = reg0.findall(text)
	r1 = reg1.findall(text)

	for x in r0:
		print("|--------[INFO][PARSER][SPAIN][NUMBER PHONE][>] " + str(x))
		config.phonesData_list.append(str(x))
	
	for x in r1:
		print("|--------[INFO][PARSER][INTERNACIONAL][NUMBER PHONE][>] " + str(x))
		config.phonesData_list.append(str(x))

def parser_IBAN(text):

	r = re.compile(r"([a-zA-Z]{2})\s*\t*(\d{2})\s*\t*(\d{4})\s*\t*(\d{4})\s*\t*(\d{2})\s*\t*(\d{10})")
	results = r.findall(text)
	if results:
		for x in results:
			print ("|--------[INFO][PARSER][IBAN][>] " + str(x))
		

def parser_EN_DATE(text):
	date = re.findall(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', text)
	if date:
		for x in date:
			print ("|--------[INFO][PARSER][DATE][>] " + str(x))
	date_barra = re.findall(r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$', text)
	if date_barra:
		for x in date_barra:
			print ("|--------[INFO][PARSER][DATE][>] " + str(x))
	date_guion = re.findall(r'\d{4}-\d{2}-\d{2}', text)
	if date_guion:
		for x in date_guion:
			print ("|--------[INFO][PARSER][DATE][>] " + str(x))

def parser_DNI(text):
	
	r = re.compile(r"(^[0-9]{8,8}[A-Za-z]$)")
	results = r.findall(text)
	if results:
		for x in results:
			print ("|--------[INFO][PARSER][DNI][>] " + str(x))
			config.DNIData_list.append(str(x))
def parserMAIN(text):

	parser_EN_DATE(text)
	parser_DNI(text)
	parser_email(text)
	parser_IBAN(text)
	parser_n_tlfn(text)