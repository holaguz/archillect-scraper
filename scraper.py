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


## open file for index recovery + parameters
'''
f = open("config.cfg", 'rt')

## load config

while (archillectIndex=='' or archillectIndex=="\n" or archillectIndex[:1]=="#"):  ## checks if the var is null, an empty line or a comment
	archillectIndex = f.readline().rstrip()
archillectIndex = int(archillectIndex)

while (minWidth == "" or minWidth == "\n" or minWidth[:1]=='#'):
	minWidth = f.readline().rstrip()

while (minHeight == '' or minHeight=='\n' or minHeight[:1]=='#'):
	minHeight = f.readline().rstrip()

f.close()
'''



## initialize browser for parsing

def scrapeImg(index):

	index = str(index)

	url = 'http://archillect.com/' + index
	print('Scraping ' + url + '...')

	r = requests.get(url)
	tree = html.fromstring(r.content)

	try:
		link = tree.xpath('//*[@id="ii"]/@src')[0] ## [0]: retrieves the first element matching the criteria
		extIndex = link.rfind(".",0) 				##search backwards looking for the first "."
		extention = link[extIndex:]		## retrieves the file extention
		
		open('img/' + index + extention , 'r') # raises FileNotFoundError exception if the file is doesn't exist
		return 1;

	except FileNotFoundError:
		print('Saving...')
		saveImg(link, index, extention)
		return 1;

	except IndexError:
		#print('[ERR] Looks like '+index+' is missing.')
		return 0;

def saveImg(link, filename, extention):

	img = requests.get(link) #load the image to memory

	fileImg = open('img/' +filename + extention, 'wb')
	fileImg.write(img.content)
	fileImg.close();

def eraseFile(filename):

	try:
		path = glob.glob('img/' + str(filename) + '.*')[0]
		os.remove(path);
	except: pass

while(0==0):

	if(scrapeImg(archillectIndex) == 1):
		archillectIndex = archillectIndex + 1
		eraseFile(archillectIndex - 61);

	else:
		config['DEFAULT']['lastIndex'] = str(archillectIndex)
		config.write(open('./config.cfg','w'));
		print('Quiting in 5...')
		#time.sleep(5);
		break;
	
	