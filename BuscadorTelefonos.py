'''
Copyright (c) 2020, QuantiKa14 Servicios Integrales S.L
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
'''

import requests, mechanize, re
from bs4 import BeautifulSoup

from search_engines import Google
from search_engines import Dogpile
from search_engines import Bing

import modules.config as C
import modules.er as R

br = mechanize.Browser()
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]

def check_facebook(phone):

	r = br.open('https://mbasic.facebook.com/')
	br.select_form(nr=0)
	br.form["email"] = phone
	br.form["pass"] = "123456"
	br.submit()
	respuestaURL = br.response().geturl()

	html =  br.response().read()
	soup = BeautifulSoup(html, "html.parser")
	a = soup.find("a",{"class":"bb"})
	if "olvidado" in R.remove_tags(str(a)):
		print("|--[INFO][FACEBOOK][CHECK][>] The account exist... \n")
	else:
		print("|--[INFO][FACEBOOK][CHECK][>] Account doesn't exist... \n")

def search_Google(phone):
	engine = Google()

	#LocateFamily
	dork = f"""site:locatefamily.com intext:"+34{phone}" OR intext:"+34{phone}" OR intext:'{phone}'"""
	print("|--[INFO][GOOGLE][DORK][RESULTS][>] " + dork)
	results = engine.search(dork)
	for r in results:
		print ("|----[INFO][GOOGLE][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"] + "\n")

	#Facebook
	dork = f"""site:facebook.com intext:"+34{phone}" OR intext:"+34{phone}" OR intext:'{phone}'"""
	print("|--[INFO][GOOGLE][DORK][RESULTS][>] " + dork)
	results = engine.search(dork)
	for r in results:
		print ("|----[INFO][GOOGLE][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"] + "\n")

	#LinkedIn
	dork = f"""site:linkedin.com intext:"+34{phone}" OR intext:"+34{phone}" OR intext:'{phone}'"""
	print("|--[INFO][GOOGLE][DORK][RESULTS][>] " + dork)
	results = engine.search(dork)
	for r in results:
		print ("|----[INFO][GOOGLE][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"] + "\n")

	#Instagram
	dork = f"""site:instagram.com intext:"+34{phone}" OR intext:"+34{phone}" OR intext:'{phone}'"""
	print("|--[INFO][GOOGLE][DORK][RESULTS][>] " + dork)
	results = engine.search(dork)
	for r in results:
		print ("|----[INFO][GOOGLE][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"] + "\n")

def search_Bing(phone):

	engine = Bing()
	results = engine.search(phone)
	for r in results:
		print ("[INFO][BING][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"] + "\n")

def search_Dogpile(phone):

	engine = Dogpile()
	results = engine.search(phone)
	for r in results:
		print ("[INFO][DOGPILE][RESULTS][>] " + r["title"] + " | " + r["text"] + " | " + r["link"] + "\n")


def attack(phone):

	check_facebook(phone)
	search_Google(phone)
	search_Bing(phone)
	search_Dogpile(phone)

def main():
	print(C.banner)

	target = input("Insert number phone: ")
	
	attack(target)

if __name__ == "__main__":
	main()
