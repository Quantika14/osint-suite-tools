#!/usr/bin/env python
# -*- coding: utf-8 -*
import mechanize, cookielib,sys, re, os, time, requests, base64
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient()
db = client.Dante

if __name__ == '__main__':
	paises=["ES","US","JP","IT","TR","GB","RU","CZ","DE","NL","KR","IL","TW","AT","CH","CA","IN","SE","NO","PL","RO","BR","AU","VN","ID","IR","UA","CN","EG","MX","TH","DK","BG","HU","SK","AR","BE","FI","IE","CL","HK","GR","CO","NZ","PT","IS","ZA","SG","LV","PK","NZ","EE","TN","SI","FO","AE","SV","PS","LT","MY","CY","CR","PH","GE","MD","KE","TT","LU","PA","KW","KZ","EC","HR","MA","MT","BD","BO","DO","AL","BA","BY","NC","RE","GT","HN","PY","VE","MN"]
	headers = {'User-Agent': 'Mozilla/5.0'}
	for pais in paises:
		url="https://www.insecam.org/en/bycountry/"+pais+"/"
		response = requests.get(url, headers=headers)
		html = response.text
		soup = BeautifulSoup(html, "html.parser")
		ul = soup.find("ul", attrs={"class":"pagination"})
		pages= int(ul.text.split(",")[1].strip())
		for i in range(pages):
			url="https://www.insecam.org/en/bycountry/"+pais+"/?page="+str(i)
			print "------------------------------------------------------------"
			print "Page: "+str(i)
			response = requests.get(url, headers=headers)
			print response
			html = response.text
			soup = BeautifulSoup(html, "html.parser")
			imgs = soup.findAll("img", attrs={"class":"thumbnail-item__img img-responsive"}) 
			for img in imgs:
				print "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
				print "Link: "+ img.get("src")
				url="https://www.insecam.org/en/view/"+str(img.get("id")).replace("image","")+"/"
				response = requests.get(url, headers=headers)
				html = response.text
				soup = BeautifulSoup(html, "html.parser")
				divs = soup.findAll("div", attrs={"class":"camera-details__cell"})
				print "Country: "+ divs[1].text.strip()
				print "Country code: "+ divs[3].text.strip()
				print "Region: "+ divs[5].text.strip()
				print "City: "+ divs[7].text.strip()
				print "Latitude: "+ divs[9].text.strip()
				print "Longitude: "+ divs[11].text.strip()
				print "ZIP: "+ divs[13].text.strip()
				print "Timezone: "+ divs[15].text.strip()
				print "Manufacturer: "+ divs[17].text.strip()
				ip_dict={"Country": divs[1].text.strip(),"Country code":divs[3].text.strip(),"Region":divs[5].text.strip(),"City":divs[7].text.strip(),"Latitude":divs[9].text.strip(),"Longitude":divs[11].text.strip(),"ZIP":divs[13].text.strip(),"Timezone":divs[15].text.strip(),"Manufacturer":divs[17].text.strip(), "link":img.get("src")}
				cursor = db.DG_cameras.update({"link":img.get("src")},ip_dict, True)
