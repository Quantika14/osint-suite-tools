#!/usr/bin/env python
# -*- coding: utf-8 -*

import requests, urllib2, re, sys
from bs4 import BeautifulSoup


user_agent = {'User-agent': 'Mozilla/5.0'}

def search_Bing(data):
	try:
		url="https://www.bing.com/search?q="+data.replace(" ", "+")
		links = SendRequest(url)
		return links
	except:
		return None

def SendRequest(url):

	try:

		response=requests.get(url,allow_redirects=True, timeout=15, verify=True)	
	except requests.exceptions.RequestException as e:
		print "\nError connection to server!",
		pass
	except requests.exceptions.ConnectTimeout as e:
		print "\nError Timeout + dork"
		pass
	content = response.text 
	return parser_html(content)

def parser_html(content):
	i = 0
	urls = []
	urls_clean = []
	urls_final = []
	delete_bing=["microsoft","msn","bing", ]
	soup = BeautifulSoup(content, 'html.parser')
	for link in soup.find_all('a'):

		try:
			href = link.get('href')
			if 'http' in href or 'https' in href:
				urls.append(href)
		except Exception as e:
			pass
	try:
		#Delete duplicates
		[urls_clean.append(i) for i in urls if not i in urls_clean] 
	except:
		pass
	try:
		#Delete not domains belongs to target
		for value in urls_clean:
			if (value.find(delete_bing[0])  == -1):
				if (value.find(delete_bing[1])  == -1):
					if (value.find(delete_bing[2])  == -1):
						urls_final.append(value)
		return urls_final
	except:
		pass
