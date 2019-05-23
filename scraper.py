import os, glob
import requests
import time
from lxml import html

import configparser

config = configparser.ConfigParser()
config.read('./config.cfg')

archillectIndex = int(config['DEFAULT']['lastIndex'])

#minWidth = ''
#minHeight = ''

if(not os.path.exists('img')): os.makedirs('img')

## initialize browser for parsing

def scrapeImg(index):

	index = str(index)

	url = 'http://archillect.com/' + index
	print('Scraping ' + url + '...')

	r = requests.get(url)
	tree = html.fromstring(r.content)

	try:
		link = tree.xpath('//*[@id="ii"]/@src')[0] 			## [0]: retrieve the first element matching the criteria
		extIndex = link.rfind(".",0) 						## search backwards looking for the first "."
		extention = link[extIndex:]							## retrieve the file extention

		open('img/' + index + extention , 'r') 				## raise FileNotFoundError exception if the file don't exist
		return 1;

	except FileNotFoundError:
		print('Saving...')
		saveImg(link, index, extention)
		return 1;

	except IndexError:
		#print('[ERR] Looks like '+index+' is missing.')
		return 0;

def saveImg(link, filename, extention):

	img = requests.get(link) 								## load the image to memory

	fileImg = open('img/' +filename + extention, 'wb')
	fileImg.write(img.content)
	fileImg.close();
def eraseFile(filename):

	try:
		path = glob.glob('img/' + str(filename) + '.*')[0]
		os.remove(path);
	except: pass

yes = 1;
while(yes):

	if(scrapeImg(archillectIndex) == 1):
		archillectIndex = archillectIndex + 1
		eraseFile(archillectIndex - 61);					## i just want to keep the last 60 imgs. TODO: add setting to cfg file

	else:
		config['DEFAULT']['lastIndex'] = str(archillectIndex)
		config.write(open('./config.cfg','w'));
		print('Quiting in 5...')
		##time.sleep(5);
		break;
