![Banner DG MINIMAL](https://quantika14.com/wp-content/uploads/2020/04/DG-minimal-version2.jpg)
Repositorio de difentes herramientas (buscadores, crawlers, bots, etc) para hacer OSINT y SOCMINT. Proyecto que tiene el objetivo de enseñar como con simples scripts en Python es posible crear una herramienta compleja que recoja y busque información para investigaciones. Para más información puedes ver los vídeos de INVESTIGA CONMIGO DESDE EL Sü
* https://www.youtube.com/watch?v=zI11NiQcx
* https://www.youtube.com/watch?v=ra-YC6MwG3k

## Buscadores

* BuscadorPersonas.py: 
  * Buscar en el BOE
  * Buscar cargos en empresas en el BORME
  * Buscar posibles cargos en empresas de familiares
  * Buscar adjudicaciones de las empresas
  * Buscar en Youtube
  * Buscar en Wikipedia
  * Buscar en Pastebin
  * Dorks en Google
  * Buscar en DuckDuckGo para obtener redes sociales y enlaces
  * Buscar en Páginas Amarillas para obtener teléfono, dirección y email
  * Conexión con la API REST de Dante's Gates

* BuscadorNoticiasFalsas.py:
  * Footprinting de la noticia
  * Búsqueda automática en Google y DuckDuckGo
  * Comparación de textos y extración de ratio de plagio
  * Búsqueda con DDG en plataformas de Fact-checking
  * Identificación de palabras claves en el texto (Ej: "informe", "estudio", etc)

* BuscadorNick.py:
  * Buscar en más de 90 plataformas
  * Buscar con DuckDuckGo
  * Conexión con la API RED de Dante's Gates

* BuscadorTelefono.py
  * Tweets
  * Check cuenta de Facebook
  * Dorks en Google
  * Identificación de compañia
  * Localización
  * Buscador de Dogpile

* BuscadorEmails (Email OSINT ripper): link ( https://github.com/Quantika14/email-osint-ripper )
  * Check cuentas en Netflix, LinkedIn, WordPress, Tumblr, Instagram, Spotify, Vimeo, Pinterest, Twitter, Flickr, Myspace, Facebook, etc
  * Análisis de reputación
  * Análisis del dominio y medidas de seguridad 
  
# ¿Cómo funciona?

1. Para su funcionamiento 100% usar sistemas Linux o Mac
1. Tener instalado Python 3
1. Tener MongoDB ````sudo apt-get install mongodb```
1. Instalar PDFGREP ```sudo apt-get install pdfgrep```
1. Instalar las dependencias ``` pip3 install -r requeriments.txt```
1. Para ejecutar cualquier buscador solo tendremos que hacer por ej: ```python3 BuscadorPersonas.py```
1. Seleccionar las diferentes configuraciones e insertar los datos que nos pida
1. Enjoy!

## Requisitos

1. Tener instalado Python 3
1. Tener instalado PDFGREP
1. Tener instalado las librerias descritas en requeriments.txt

# Autor
* Jorge Coronado a.k.a Jorge Websec
* Twitter: @JorgeWebsec
* Web: www.quantika14.com
