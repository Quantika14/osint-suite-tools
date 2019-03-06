#!Library/Frameworks/Python.framework/Versions/2.7/bin/python
import os
import sys
import urllib2
import urllib
import urlparse
import argparse
import Queue

from cgi import escape
from traceback import format_exc
from BeautifulSoup import BeautifulSoup

MIME_TYPE = ('.pdf',)
URL_TYPE = ('.html', '.htm', '')

MAX_LOOP = 5000
l = 0
crawl_history = []
url_queue = Queue.Queue()
fetch_queue = Queue.Queue()


def isMime(input):
  for type in MIME_TYPE:
    if type == input:return True
  return False


def isUrl(input):
  for type in URL_TYPE:
    if type == input:return True
  return False

def parse(url, context=''):
  try:
    soup = BeautifulSoup(context)
    tags = soup('a')

    for tag in tags:
      href = tag.get('href')
      ##if href.startswith('/') or (href.find('/') == -1) or (href.startswith('./')) or (href.startswith('../')): #if relative path, then normalize
      href = urlparse.urljoin(url, href)

      href_path = urlparse.urlparse(href).path
      ext = os.path.splitext(href_path)[1]
      
      #check type
      if href in crawl_history:continue

      if isMime(ext): fetch_queue.put(href)
      if isUrl(ext): url_queue.put(href)
  except Exception as e:
    print e 


def fetch(dir):
  try:
    if os.path.exists(dir) == False:
      os.makedirs(dir)
    while fetch_queue.empty() == False :
      data_url = fetch_queue.get()
      file_path = dir + '/' + data_url.split('/')[-1]
      try:
        if __debug__: print 'going to fetch: ' + data_url
        urllib.urlretrieve(data_url, file_path) #urllib2 raise error Todo:
      except:
        print 'error at fetching '+data_url
        continue

  except Exception as e:
    print e  


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description = 'pdf fetch script')
  parser.add_argument('directory', help = 'save directory')
  parser.add_argument('starturl', help = 'start url')

  args = parser.parse_args()
  dir = args.directory

  url_queue.put(args.starturl) #initilize startup url

  print 'start crawling: '
  while (l<MAX_LOOP) :
    ++l
    if url_queue.empty():
      break 
    else:
      cur_url = url_queue.get()
      if __debug__: 'start crawl: '+cur_url
      try: 
        response = urllib2.urlopen(cur_url)
        ret = response.read()
        parse(cur_url,ret)
        fetch(dir)                   
      
      except Exception as e:
        print e

