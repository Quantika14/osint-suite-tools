#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, requests, dryscrape, time, urllib2, ssl
from pymongo import MongoClient
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from urllib2 import Request
import tabula
reload(sys)
sys.setdefaultencoding("utf8")
client = MongoClient(connect=False)
db = client.Dante

url="https://sedeapl.dgt.gob.es"
num_edict=0
time_to_next=1

sess = dryscrape.Session(base_url = url)
sess.visit('WEB_TTRA_CONSULTA/Todos.faces?idioma=es')
sess.set_attribute('auto_load_images', False)

def extract_linkPDF(link):
	try:
		global sess
		sess.visit(link)
		link_pdf=sess.at_xpath("/html/body/div/div2]/a")
		return link_pdf.get_attr("href")
	except Exception as e:
		print "ERROR]EXTRACT_LINKPDF]>] "+str(e)
		return None

def extract_date(download_url):
	print download_url
	pdf = tabula.read_pdf(download_url, guess=False,  output_format="json",pages ="all", nospreadsheet=True)
	for page in pdf:
		for line in page"data"]:
			for i in range(len(line)):
				try:
					if "Núm. "in linei]"text"]:
						return linei+1]"text"].split("Pág")0].strip().replace(" ","_")
				except Exception as e:
					print "ERROR]EXTRACT_DATE]>] "+str(e)
					continue
	return "no_date"

def next_page():
	try:
		but_next_page=sess.at_xpath('//*@id="paginacion:siguiente"]')
		but_next_page.click()
		time.sleep(1)
	except Exception as e:
		print "ERROR]NEXT PAGE]>] "+str(e)
		print "SEVERAL ERROR]"

def insert_mongo(dict_testra):
	cursor=db.DG_testra.update({"dni":dict_testra"dni"]},dict_testra,True)
	print cursor
	print dict_testra


def extract_links():
	global sess
	try:
		links=list()
		html=sess.body()
		soup=BeautifulSoup(html, "html.parser")
		aes=soup.findAll("a")
		for a in aes:
			if "http://" not in a.get("href") and "sedeapl.dgt" not in a.get("href"):
				links.append(a.get("href"))
		return links
	except Exception as e:
		print "ERROR]EXTRACT_LINKS]>] "+str(e)
		return None

def download_pdfs(links):
	global num_edict
	for link in links:
		try:
			download_url=extract_linkPDF(link)
			if download_url:
				date_edict=extract_date("https://sedeapl.dgt.gob.es"+download_url)
				context = ssl._create_unverified_context() #SSLContext(ssl.PROTOCOL_TLSv1)
				response = urllib2.urlopen("https://sedeapl.dgt.gob.es"+download_url, context=context)
				namef = "EDICTO-"+date_edict+""+str(num_edict)+"].pdf"
				num_edict+=1
				file = open("PDFS/"+namef, 'w')
				file.write(response.read())
				file.close()
				print("Download] -> " + download_url, namef)
				convert_pdf_to_txt("PDFS/"+namef)
		except Exception as e:
			print "ERROR]DOWNLOAD PDF]>] "+str(e)
			continue

def convert_pdf_to_txt(path):
	try:
		pdf = tabula.read_pdf(path, guess=False,  output_format="json",pages ="all", nospreadsheet=True)
		for page in pdf:
			for line in page"data"]:
				if len(line)>=4:
					if line0]"text"]!='' and line2]"text"] != '' and line3]"text"] != "REQ" and line0]"text"]!='EXPEDIENTE SANCIONADO/A':
						name=""
						surname=""
						dni=None
						localidad=""
						matricula=""
						if "," in line0]'text']12:]: 
							namec_split = line0]'text']12:].split(",")
							for names in namec_split1].split():
								if str(names:len(names)-1]).isdigit():
									dni=names
								else:
									name+=" "+names
							for surnames in namec_split0].split():
								if surnames.isdigit():
									pass
								else:
									surname+=" "+surnames
							name=name.strip()
							surname=surname.strip()
						else:
							for names in line0]'text']12:].split():
								if names.isdigit():
									dni=names
								else:
									name+=" "+names
							name=name.strip()
							surname=""
						data=line1]"text"].split()
						expediente=line0]"text"]:12]
						validator=False
						if dni != None:
							for d in range(len(data)):
								if validator==False:
									if "/" not in datad]:
										localidad+=datad]+" "
									else:
										validator=True
								else:
									if datad].isdigit():
										if datad+1] == "RGC" or datad+1]=="LSV" or datad+1]=="OGC" or datad+1]=="RDL" or datad+1]=="RD":
											break
										else:
											matricula+=datad]
									else:
										matricula+=datad]
						else:
							for d in range(1,len(data)):
								if validator==False:
									if "/" not in datad]:
										localidad+=datad]+" "
									else:
										validator=True
								else:
									if datad].isdigit():
										if len(datad+1])<4:
											if datad+1] == "RGC" or datad+1]=="LSV" or datad+1]=="OGC" or datad+1]=="RDL" or datad+1]=="RD":
												break
										else:
											matricula+=datad]
									else:
										matricula+=datad]
						if dni==None:
							dni=data0]
						print "Expediente: "+expediente.strip()
						print "Nombre: "+name+" "+surname
						print "DNI: "+dni.strip()
						print "Matricula: "+matricula.strip()
						print "Localidad: "+localidad.strip()
						dict_testra={"expediente":expediente.strip(),"nombre":name+" "+surname,"dni":dni.strip(),"matricula":matricula.strip(), "localidad":localidad.strip()}
						print "Mongo>]"
						insert_mongo(dict_testra)
						print "-----------------*****************************************-------------"
	except Exception as e:
		print "ERROR]CONVERT_PDF]>] "+str(e)

if __name__ == '__main__':
	while(next):
		try:
			links=extract_links()
			url=sess.url()
			if links:
				download_pdfs(links)
			sess.visit('WEB_TTRA_CONSULTA/Todos.faces?idioma=es')
			for i in range(time_to_next):
				next_page()
			time_to_next+=1
			time.sleep(2)
		except Exception as e:
			print "ERROR]MAIN]>] "+str(e)
			time.sleep(10)	
