import urllib2, requests, time, os, re, ssl, threading, hashlib, sys
from bs4 import BeautifulSoup
from pymongo import MongoClient
from time import sleep
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from threading import Lock
reload(sys)
sys.setdefaultencoding('utf-8')

header = {'User-agent':'Mozilla/5.0'}
lock = Lock()
ano = 1966 #Primero - 1961 
i = 14444 #Empezar en 1
dif = 3000
count_global= 0
th = []
pdf_urls = []
url = "https://www.boe.es/diario_boe/txt.php?id=BOE-A-"
count = 0
client = MongoClient(connect=False)
db = client.Dante
m = hashlib.md5()

def insert_mongo(nombre, text, enlace, hash_pdf):
	pdf=db.DG_boe.find_one({"text":text})
	if pdf == None:
		db.DG_boe.update({'text':text},{"nombre":nombre,"text":text, "enlace":enlace, "hash":hash_pdf}, True)
	else:
		db.DG_boe.update({'text':text},{"$set":{"hash":hash_pdf}}, True)
	print "[INFO] Insertado correctamente"
	remove_file(nombre)

def log_pdf(url):
	f = open("log_error.txt", "a")
	f.write(url+"\n")
	f.close()

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)

def decript_pdf(namef):
	command="qpdf --password= --decrypt boe_pdf/"+namef+" boe_pdf/d_"+namef
	os.popen(command)
	return "d_"+namef

#funcion que pasa de anos si las url no devuelven nada cada 3000
def jump(var):
	global count_global
	if var == True:
		count_global+=1
	else:
		pass
	return count_global

def convert_pdf_to_txt(path):
	try:
		rsrcmgr = PDFResourceManager()
		retstr = StringIO()
		codec = 'utf-8'
		laparams = LAParams()
		device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
		fp = file(path, 'rb')
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		password = ""
		maxpages = 0
		caching = True
		pagenos=set()

		for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
			interpreter.process_page(page)

		text = retstr.getvalue()

		fp.close()
		device.close()
		retstr.close()
		return text
	except Exception as e:
		print e
		nombre=path.split("/")[1]
		remove_file(nombre)
		return False

def download_file(download_url,ano,mes,dia,i):
	print download_url
	context = ssl._create_unverified_context() #SSLContext(ssl.PROTOCOL_TLSv1)
	response = urllib2.urlopen(download_url, context=context)
	namef = "BOE-A-"+dia+"-"+mes+"-"+ano+"-"+str(i)+".pdf"
	file = open("boe_pdf/"+namef, 'w')
	file.write(response.read())
	file.close()
	print("[Download] -> " + download_url, namef)
	return namef

def remove_file(nombre):
	ruta = "boe_pdf/" + nombre
	os.remove(ruta)

def file_as_bytes(file):
	with file:
		return file.read()


def worker():
	global count, i, ano, count_global
	while (ano < 2019):
		while(i < 320001):
			try:
				url_ = url + str(ano) + "-"+ str(i)
				print url_
				response = requests.get(url_, headers=header)
				html = response.text
				soup = BeautifulSoup(html, "html.parser")
				link_pdf = soup.find("li",{"class":"puntoPDFsup"})
				pdf_u = "https://www.boe.es"+ link_pdf.a.get('href')
				year = pdf_u.split('/')[5]
				mes = pdf_u.split('/')[6]
				dia = pdf_u.split('/')[7]

				try:
					response = urllib2.urlopen(pdf_u)
					if "404" in str(response):
						print 'Error in PDF url.'
						continue
					else:
						namef=download_file(pdf_u,year,mes,dia,count)
						text=convert_pdf_to_txt("boe_pdf/"+namef)
						hash_pdf=hashlib.md5(file_as_bytes(open("boe_pdf/"+namef,'rb'))).hexdigest()
						if text:
							insert_mongo(namef, text, pdf_u, hash_pdf)
							sleep(2)
							count += 1
							count_global = 0
						else:
							print "[INFO][>] No es un pdf"
						sleep(3)
					sleep(2)
					lock.acquire()
					i += 1
					lock.release()
				except Exception as e:
					print e
					lock.acquire()
					i += 1
					count=jump(True)
					jump(True)
					if count_global>=dif:
						ano+=1
						count_global=1
						i=1
					lock.release()
					continue
			except Exception, error:
				#print error
			 	print 'Error in url, continue...'
				lock.acquire()
				i += 1
				jump(True)
				if count_global>=dif:
					ano+=1
					count_global=1
					i=1
				lock.release()
				continue
		lock.acquire()
		ano += 1
		i=1
		lock.release()
def main():
	for i in range(1):
		th.append(threading.Thread(target=worker))
		th[i].start()

if __name__ == '__main__':
	main()
