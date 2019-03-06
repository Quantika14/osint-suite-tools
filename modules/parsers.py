#!/usr/bin/env python
# -*- coding: utf-8 -*
import re

def parser_email(text):
	# regex = something@whatever.xxx
	r = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')
	results = r.findall(text)
	if results:
		for x in results:
				print "|--------[INFO][PARSER][EMAIL][>] " + str(x)


def parser_n_tlfn(text):
	#Para buscar dentro de un texto
	reg0 = re.compile(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?")
	#Para buscar con la extension
	reg1 = re.compile("\d{3}\d{3}\d{4}")
	#Para buscar entre espacios y delimitadores
	reg2 = re.compile(".*?(\(?\d{3})? ?[\.-]? ?\d{3} ?[\.-]? ?\d{4}).*?", re.S)
	
	r0 = reg0.findall(text)
	r1 = reg1.findall(text)
	r2 = reg2.findall(text)

	for x in r0:
		print "|--------[INFO][PARSER][EMAIL][>] " + str(x)
	
	for x in r1:
		print "|--------[INFO][PARSER][EMAIL][>] " + str(x)
	
	for x in r2:
		print "|--------[INFO][PARSER][EMAIL][>] " + str(x)