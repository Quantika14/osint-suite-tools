import re

def replace_acentos(cadena):
    cadena = cadena.upper()
    cadena=cadena.replace('Á','A');
    cadena=cadena.replace('É','E');
    cadena=cadena.replace('Í','I');
    cadena=cadena.replace('Ó','O');
    cadena=cadena.replace('Ú','U');
    cadena=cadena.replace('Ñ','N');
    cadena=cadena.replace('Ä','A');
    cadena=cadena.replace('Ë','E');
    cadena=cadena.replace('Ï','I');
    cadena=cadena.replace('Ö','O');
    cadena=cadena.replace('Ü','U');
    return cadena.lower()

def replace_letras_raras(cadena):
    cadena = cadena.upper()
    cadena = cadena.replace("Ñ", "N")
    return cadena.lower()

# Eliminar tags HTML
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)

