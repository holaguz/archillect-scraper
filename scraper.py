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
img_dir = "./img/"
#minWidth = ''
#minHeight = ''

if not os.path.exists(img_dir): os.makedirs(img_dir)

def scrapeImg(index):

	index = str(index)

	url = baseAddress + index
	r = requests.get(url)
	tree = html.fromstring(r.content)

	try:
		link = tree.xpath('//*[@id="ii"]/@src')[0] 								## [0]: retrieve the first element matching the criteria
		extIndex = link.rfind(".",0) 											## search backwards looking for the first "."
		fileExtention = link[extIndex:]											## retrieve the file basetype
		fileName = index + fileExtention
		return fileName;

	except IndexError:
		print('Looks like '+ baseAddress + str(index) +' is not valid.')
		return -1;

def saveImg(fileName):

	if fileName in os.listdir(img_dir): return 0;

	fileAddress = baseAddress + fileName
	print("Saving " + fileAddress)
	file = requests.get(fileAddress) 											## load the file to memory
	
	with open(img_dir + fileName, 'wb') as f: 
		f.write(file.content)
		f.close();

def eraseFiles():
	try:
		fileList = os.listdir("./img")
		while(len(fileList) > imgCount):
			
			os.remove("./img/" + fileList[0])
			fileList = os.listdir("./img")
	except: pass

def searchIndex():

	step = imgCount;
	index = ndx;
	
	while(True):
		print("Searching last index... Current index: " + str(index) + " step " + str(step) + "... ", end='')
		if scrapeImg(index) == -1:  											## when the index is not valid we go backwards
			index -= step
			step = int(step/2)
			if step == 0 : return index
		else: 
			index += step;
			print('Index is valid, continue search')


ndx = searchIndex()																## main loop
print('Found index: ' + str(ndx))
ndx -= imgCount

while(True):
	
	f = scrapeImg(ndx)
	print('Scraping ' + baseAddress + str(ndx) + '...')

	if f != -1:
		saveImg(f)
		ndx += 1
	else:
		print("Erasing extra files...")
		eraseFiles();

		config['DEFAULT']['lastIndex'] = str(ndx)
		#config['DEFAULT']['imgCount'] = str(imgCount)
		config.write(open('./config.cfg','w'));
		
		print('Quiting in 5...')
		##time.sleep(5);
		break;
