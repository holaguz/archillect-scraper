import os, glob
import requests
import time
from lxml import html

import configparser

config = configparser.ConfigParser()
config.read('./config.cfg')

ndx = int(config['DEFAULT']['lastIndex'])
imgCount = int(config['DEFAULT']['imgCount'])
baseAddress = 'http://archillect.com/'
#minWidth = ''
#minHeight = ''

if(not os.path.exists('img')): os.makedirs('img')

## initialize browser for parsing

def scrapeImg(index, save):

	index = str(index)

	url = baseAddress + index
	print('Scraping ' + url + '...')

	r = requests.get(url)
	tree = html.fromstring(r.content)

	try:
		link = tree.xpath('//*[@id="ii"]/@src')[0] 			## [0]: retrieve the first element matching the criteria
		extIndex = link.rfind(".",0) 						## search backwards looking for the first "."
		filenameExtention = link[extIndex:]							## retrieve the file filenameExtention
		if save: open('img/' + index + filenameExtention , 'r') 				## raise FileNotFoundError exception if the file don't exist
		return 1;

	except FileNotFoundError:
		print('Saving...')
		saveImg(link, index, filenameExtention)
		return 1;

	except IndexError:
		print('[ERR]: Looks like '+ baseAddress + str(index) +' is not valid.')
		return 0;

def saveImg(link, filename, filenameExtention):
	img = requests.get(link) 								## load the image to memory
	fileImg = open('img/' + filename + filenameExtention, 'wb')
	fileImg.write(img.content)
	fileImg.close();

def eraseFile():
	try:
		fileList = os.listdir(".img/")
		os.remove(fileList[0])
		#path = glob.glob('img/' + str(filename) + '.*')[0]
		#os.remove(path);
	except: pass

def searchIndex():
	#iterate over indexes on the website
	step = imgCount;
	index = ndx;
	
	while(True):
		print("\nSearching last index... Current index: " + str(index) + " step " + str(step))

		if(scrapeImg(index, False) == 0):  # Si el indice no es valido vuelvo hacia atras y reduzco el paso
			index -= step
			step = int(step/2)
			if step == 1 : return index
		else: 
			index += step;
			print('Index is valid, continue search')




ndx = searchIndex()
print('Found index: ' + str(ndx))

while(True):
	

	if(scrapeImg(ndx, True) == 1):
		ndx = ndx + 1
		eraseFile();

	else:
		config['DEFAULT']['lastIndex'] = str(ndx)
		config['DEFAULT']['imgCount'] = str(imgCount)
		config.write(open('./config.cfg','w'));
		print('Quiting in 5...')
		##time.sleep(5);
		break;
